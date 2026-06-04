# Laporan Proof of Concept (PoC): Implementasi Wazuh SIEM, Suricata IDS, dan Shuffle SOAR untuk Deteksi serta Otomatisasi Respon terhadap DDoS di Microsoft Azure

## Anggota Kelompok

| Nama							| NRP			|
|-------------------------------|---------------|
| Muhammad Rakha Hananditya R.	| 5027241015	|
| Muhammad Afrizan Rasya	| 5027241048	|
| Ni'mah Fauziyyah Atok	| 5027241103	|

## Daftar Isi

## I: Pendahuluan

<p align="justify"> &emsp;Projek ini bertujuan untuk membuktikan bahwa <b>platform keamanan <i>open-source</i></b> dapat diimplementasikan untuk mendeteksi dan secara otomatis memblokir serangan jaringan, khususnya <b>Distributed Denial of Service (<i>DDoS</i>)</b>. Dalam projek ini, digunakanlah <code>Wazuh</code> sebagai <b>Security Information and Event Management (<i>SIEM</i>)</b> dan <code>Suricata</code> sebagai <b>Network Intrusion Detection System (<i>NIDS</i>)</b>.
</p>

<p align="justify"> &emsp;<b>Proof of Concept (<i>PoC</i>)</b> ini digunakan untuk menyatakan bukti terhadap setiap langkah konfigurasi dari awal pembuatan <code>Virtual Machine (VM)</code> di <code>Azure</code>, konfigurasi yang dilakukan, hingga hasil akhir pengujian simulasi <i>DDoS</i>. Adapun, topologi yang digunakan mencakup satu <code>VNet Azure (10.0.0.0/24)</code> dengan menggunakan tiga machine: </p> <ol> <li> <p align="justify"> <b>VM 1 (<code>Wazuh Manager</code>)</b>: Menjalankan <code>Wazuh Server</code>, <code>Indexer</code>, dan <code>Dashboard</code> yang memiliki <b>IP Publik</b> dan <b>Privat</b> sekaligus. </p> </li> <li> <p align="justify"> <b>VM 2 (<code>Wazuh Agent 1</code> / <i>Attacker</i>)</b>: Bertindak sebagai penyerang menggunakan <code>Apache Bench</code>. Hanya memiliki <b>IP Privat</b>. </p> </li> <li> <p align="justify"> <b>VM 3 (<code>Wazuh Agent 2</code> / <i>Victim</i>)</b>: Bertindak sebagai target serangan yang dipasangi <code>Web Server NGINX</code> dan <code>Suricata IDS</code>. Hanya memiliki <b>IP Privat</b>. </p> </li> </ol>

## II: Persiapan Infrastruktur Cloud di Microsoft Azure

<p align="justify"> &emsp; Tahap pertama adalah menyiapkan <b><i>environment</i></b> di portal <code>Azure</code> menggunakan akun <code>Microsoft Azure for Students</code>. Kemudian masuk ke dalam <code>Compute Infrastructure → Virtual Machines → Create → Virtual machine</code> untuk membuat <code>Virtual Machine (VM)</code> baru. </p> <p align="justify"> &emsp; Kemudian di halaman Di halaman <code>Create Virtual Machine</code>, konfigurasikan masing-masing <code>VM</code> sesuai dengan konfigurasi yang tertera di bawah, dengan catatan semua <code>VM</code> ditempatkan dalam satu <code>Resource Group</code> yang sama dengan nama <code>WazuhManager_group</code>. </p> <p align="justify"> &emsp; <b>a. Konfigurasi VM 1 (Wazuh Manager)</b> </p> <ol> <li> <p align="justify"> Di tab <code>Basics</code>, tetapkan <code>resource group</code> baru yang nantinya akan digunakan pada <code>VM Wazuh Agent</code> juga. </p> </li>
<li>
	<p align="justify">
		Pilih OS <code>Ubuntu Server 24.04 LTS - x64 Gen2</code> dan <code>Size Standard_D2s_v3 (2 vCPU, 8 GiB RAM)</code>. Pemilihan resource didasarkan karena <code>VM Wazuh Manager</code> membutuhkan resource yang cukup besar untuk menjalankan database <code>OpenSearch</code> via <code>Wazuh Indexer</code>.
	</p>
</li>

<li>
	<p align="justify">
		Tetapkan region sebagai <code>(Asia Pacific) East Asia</code> dengan tidak menerapkan redudansi 3 infrastruktur dan keamanan sebagai <code>Standard</code>.
	</p>
</li>

<li>
	<p align="justify">
		Tetapkan hibernasi sebagai mati. Hal ini didasari bahwasannya <code>VM</code> digunakan untuk <b><i>SIEM</i></b> di mana perlu melakukan monitoring penuh dalam kurun waktu yang terus menerus agar tidak ada informasi yang terlewat.
	</p>
</li>

<li>
	<p align="justify">
		Tetapkan otentikasi menggunakan <code>Password</code> dan aktifkan akses terhadap port <code>22</code> milik <code>SSH</code> untuk memudahkan akses ke dalam <code>VM</code>.
	</p>
</li>

<li>
	<p align="justify">
		Di tab <code>Disks</code>, matikan enkripsi, dan biarkan ukuran penyimpanan sesuai dengan default yang sudah ditetapkan.
	</p>
</li>

<li>
	<p align="justify">
		Di tab <code>Networking</code>, buat <code>VNet</code> baru bernama <code>WazuhManager-vnet</code> dengan subnet <code>10.0.0.0/24</code>. Untuk <code>VM</code> ini, akan dibuat juga <code>Public IP</code> baru.
	</p>
</li>

<li>
	<p align="justify">
		Klik <code>Review + create</code> dan tunggu proses selesai.
	</p>
</li>
</ol>

<p align="justify"> &emsp; Setelah <code>VM</code> dijalankan, langkah selanjutnya adalah melakukan konfigurasi terhadap pengaturan jaringan, di mana beberapa port spesifik perlu dibukan pada <code>Network Security Group (NSG)</code> agar kedua <code>Wazuh Agent</code> bisa berkomunikasi dengan <code>Wazuh Manager</code> dan <code>Dashboard</code> bisa diakses. Navigasi ke menu <code>Networking → Network settings → Create port rule → Inbound port rule</code> di <code>VM</code> tersebut dan tambahkan tiga <code>Inbound Port Rules</code>: </p> <ul> <li> <p align="justify"> <b>AllowWazuhDashboard</b>: </p>
	<ul>
		<li>
			<p align="justify">
				<code>Source</code> : <code>any</code>
			</p>
		</li>
		<li>
			<p align="justify">
				<code>Source port ranges</code> : <code>*</code>
			</p>
		</li>
		<li>
			<p align="justify">
				<code>Destination</code> : <code>any</code>
			</p>
		</li>
		<li>
			<p align="justify">
				<code>Service</code> : <code>HTTPS</code>
			</p>
		</li>
		<li>
			<p align="justify">
				<code>Destination port ranges</code> : <code>443</code>
			</p>
		</li>
		<li>
			<p align="justify">
				<code>Protocol</code> : <code>TCP</code>
			</p>
		</li>
		<li>
			<p align="justify">
				<code>Action</code> : <code>Allow</code>
			</p>
		</li>
		<li>
			<p align="justify">
				<code>Priority</code> : <code>200</code>
			</p>
		</li>
		<li>
			<p align="justify">
				<code>Name</code> : <code>AllowWazuhDashboard</code>
			</p>
		</li>
	</ul>
</li>

<li>
	<p align="justify">
		<b>AllowAgentEnrollment</b>:
	</p>
	<ul>
		<li>
			<p align="justify">
				<code>Source</code> : <code>Service Tag</code>
			</p>
		</li>
		<li>
			<p align="justify">
				<code>Source service tag</code> : <code>VirtualNetwork</code>
			</p>
		</li>
		<li>
			<p align="justify">
				<code>Source port ranges</code> : <code>*</code>
			</p>
		</li>
		<li>
			<p align="justify">
				<code>Destination</code> : <code>any</code>
			</p>
		</li>
		<li>
			<p align="justify">
				<code>Service</code> : <code>Custom</code>
			</p>
		</li>
		<li>
			<p align="justify">
				<code>Destination port ranges</code> : <code>1515</code>
			</p>
		</li>
		<li>
			<p align="justify">
				<code>Protocol</code> : <code>TCP</code>
			</p>
		</li>
		<li>
			<p align="justify">
				<code>Action</code> : <code>Allow</code>
			</p>
		</li>
		<li>
			<p align="justify">
				<code>Priority</code> : <code>202</code>
			</p>
		</li>
		<li>
			<p align="justify">
				<code>Name</code> : <code>AllowAgentEnrollment</code>
			</p>
		</li>
	</ul>
</li>

<li>
	<p align="justify">
		<b>AllowAgentTraffic</b>:
	</p>
	<ul>
		<li>
			<p align="justify">
				<code>Source</code> : <code>Service Tag</code>
			</p>
		</li>
		<li>
			<p align="justify">
				<code>Source service tag</code> : <code>VirtualNetwork</code>
			</p>
		</li>
		<li>
			<p align="justify">
				<code>Source port ranges</code> : <code>*</code>
			</p>
		</li>
		<li>
			<p align="justify">
				<code>Destination</code> : <code>any</code>
			</p>
		</li>
		<li>
			<p align="justify">
				<code>Service</code> : <code>Custom</code>
			</p>
		</li>
		<li>
			<p align="justify">
				<code>Destination port ranges</code> : <code>1514</code>
			</p>
		</li>
		<li>
			<p align="justify">
				<code>Protocol</code> : <code>TCP</code>
			</p>
		</li>
		<li>
			<p align="justify">
				<code>Action</code> : <code>Allow</code>
			</p>
		</li>
		<li>
			<p align="justify">
				<code>Priority</code> : <code>201</code>
			</p>
		</li>
		<li>
			<p align="justify">
				<code>Name</code> : <code>AllowAgentTraffic</code>
			</p>
		</li>
	</ul>
</li>
</ul>
<p align="justify"> &emsp; Selain itu, Agar IP lokal tidak berubah saat restart, masuk ke pengaturan <code>Network Interface → Wazuh Manager → Configure your IPs → ipconfig1 → Private IP address settings</code>, dan 5 kemudian mengubah ke <code>Private IP</code> menjadi <code>Static</code>. </p> <p align="justify"> &emsp; <b>b. Konfigurasi VM 2 (Wazuh Agent 1) dan VM 3 (Wazuh Agent 2)</b> </p> <ol> <li> <p align="justify"> Secara keseluruhan, proses pembuatan <code>VM 2</code> dan <code>3</code> hampir sama dengan <code>VM 1</code>, hanya saja dengan spesifikasi lebih rendah (<code>Standard_B2as_v2</code>) dan tanpa <code>Public IP</code> demi keamanan. </p> </li>
<li>
	<p align="justify">
		Buat <code>VM 2</code> dengan nama <code>WazuhAgent1</code> dan <code>VM 3</code> dengan nama <code>WazuhAgent2</code>. Kedua <code>VM</code> menggunakan <code>resource group</code> yang sudah ditetapkan sebelumnya di <code>VM Wazuh Manager</code>.
	</p>
</li>

<li>
	<p align="justify">
		Di tab <code>Networking</code>, pastikan memilih <code>VNet WazuhManager-vnet</code> yang sudah dibuat pada <code>VM</code> sebelumnya dan atur <code>Public IP</code> ke <code>None</code>.
	</p>
</li>

<li>
	<p align="justify">
		Klik <code>Review + create</code> dan tunggu proses selesai.
	</p>
</li>
</ol> <p align="justify"> &emsp; Setelah <code>VM</code> berhasil dibuat, langkah selanjutnya adalah masuk ke dalam <code>Network Interface</code> masing-masing dan atur <code>Private IP</code> menjadi <code>Static</code>. </p> <p align="justify"> &emsp; Dikarenakan kedua <code>VM Agent</code> tidak memiliki <code>IP</code> publik, akses <code>SSH</code> dapat dilakukan dengan metode <b><i>jump host</i></b> dari <code>VM Wazuh Manager</code>. </p>

```sh
# Akses dari console ke Wazuh Manager
ssh azureuser@<Public-IP-VM1>

# Dari dalam Manager, SSH ke Agent
ssh azureuser@<Private-IP-VMAgent1>

# atau
ssh azureuser@<Private-IP-VMAgent2>
```

## III: Instalasi Wazuh All-in-One (VM 1)

## IV: Wazuh Custom Rules dan Active Response (VM 1)

## V: Instalasi Wazuh Agent (VM 2 dan 3)

## VI: Instalasi dan Konfigurasi Suricata dan NGINX (VM 3)

## VII: Konfigurasi Pembacaan Logfile (VM 3)

## VIII: Instalasi Apache Bench dan Simulasi DDoS (VM 2)

## IX: Instalasi Docker dan Shuffle (VM 4)

## X: Konfigurasi Webhook Wazuh (VM 1)

## XI: Implementasi Workflow Shuffle (VM 4)

## XII: Pembaruan Active Response Wazuh (VM 3)

## XIII: Pengujian Workflow Shuffle

## XIV: Penutup

