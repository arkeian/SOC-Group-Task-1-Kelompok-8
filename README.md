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

## II: Persiapan Infrastruktur Cloud SIEM di Microsoft A
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

## II: Persiapan Infrastruktur Cloud SIEM di Microsoft Azure

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

<p align="justify"> &emsp; <code>Wazuh</code> menyediakan script instalasi otomatis yang mempermudah setup <code>Wazuh Indexer</code>, <code>Manager</code>, dan <code>Dashboard</code> dalam satu server sekaligus. Di mana langkah implementasinya: </p> <ol> <li> <p align="justify"> <code>SSH</code> ke <code>VM 1</code> menggunakan kredensial yang sudah ditetapkan. </p> </li>
<li>
	<p align="justify">
		Unduh installer dan aktifkan <code>Wazuh</code>:
	</p>
</li>
</ol>

```sh
# Install Wazuh Manager, Dashboard, dan Indexer
curl -sO https://packages.wazuh.com/4.14/wazuh-install.sh && sudo bash ./wazuh-install.sh -a

# Mengaktifkan Wazuh Manager, Dashboard, dan Indexer
sudo systemctl enable wazuh-manager
sudo systemctl enable wazuh-indexer
sudo systemctl enable wazuh-dashboard

sudo systemctl start wazuh-manager
sudo systemctl start wazuh-indexer
sudo systemctl start wazuh-dashboard
```

<p align="justify"> &emsp; Setelah proses instalasi selesai, <code>Wazuh</code> akan menyediakan kredensial <code>username</code> dan <code>password</code> default yang akan digunakan untuk mengakses <code>Wazuh Dashboard</code> dalam browser. </p>

## IV: Wazuh Custom Rules dan Active Response (VM 1)

<p align="justify"> &emsp; Pada tahap ini dilakukan pengaturan tambahan pada <code>Wazuh</code> agar sistem tidak hanya berfungsi sebagai pusat pemantauan log, tetapi juga mampu melakukan respons otomatis terhadap pola serangan yang terdeteksi. Hal ini dilakukan dengan menerapkan <b><i>active response</i></b> dan <b><i>custom rules</i></b> pada konfigurasi <code>Wazuh Manager</code>. </p> <p align="justify"> &emsp; Langkah pertama adalah melakukan konfigurasi <b><i>active response</i></b> pada file <code>/var/ossec/etc/ossec.conf</code>, dengan konfigurasi pemblokiran umum melalui <code>firewall-drop</code> dan respons jalur khusus untuk alert yang berasal dari <code>Suricata</code>. </p>

```xml
<command>
  <name>suricata-firewall-drop</name>
  <executable>suricata-firewall-drop</executable>
  <timeout_allowed>yes</timeout_allowed>
</command>
```

<p align="justify"> &emsp; Mendefinisikan <b><i>custom command</i></b> pada <code>Wazuh</code> yang nantinya akan dipanggil oleh mekanisme <b><i>active response</i></b> ketika rule tertentu ke trigger. Command <code>suricata-firewall-drop</code> dibuat secara khusus untuk menangani alert yang berasal dari <code>Suricata</code>. </p>

```xml
<active-response>
  <disabled>no</disabled>
  <command>firewall-drop</command>
  <location>local</location>
  <rules_id>5712,5720,5763,100100,100110</rules_id>
  <timeout>1800</timeout>
  <repeated_offenders>30, 60, 120, 180, 240, 360, 720, 1440</repeated_offenders>
</active-response>
```

<p align="justify"> &emsp; Bagian ini mengaktifkan fitur <b><i>active response</i></b> <code>Wazuh</code> untuk memutus koneksi dari pemicu rule spesifik secara otomatis. Pengaturan <code>location local</code> memastikan tindakan dilakukan langsung pada host sumber alert agar pemblokiran lebih relevan. Konfigurasi ini mencakup daftar <code>rules_id</code> pemicu, <code>timeout</code> blokir secara incremental di mulai dari selama 30 menit hingga 1 hari, serta mekanisme <code>repeated_offenders</code> untuk eskalasi durasi bagi penyerang berulang. </p>

```xml
<active-response>
  <disabled>no</disabled>
  <command>suricata-firewall-drop</command>
  <location>local</location>
  <rules_id>86681, 100200, 100201, 100202, 100203, 100204, 100205, 100208</rules_id>
  <timeout>1800</timeout>
  <repeated_offenders>30, 60, 120, 180, 240, 360, 720, 1440</repeated_offenders>
</active-response>
```

<p align="justify"> &emsp; Konfigurasi <b><i>active response</i></b> ini dikhususkan untuk mitigasi <i>DDoS</i> berbasis <code>Suricata</code>. Penggunaan command <code>suricata-firewall-drop</code> diperlukan karena format log <code>JSON NIDS</code> yang berbeda. </p> <p align="justify"> &emsp; Selanjutnya, logika deteksi diperluas melalui <b><i>custom rules</i></b> pada <code>/var/ossec/etc/rules/local_rules.xml</code>. Penambahan ini menyatukan log <code>SSH</code>, <code>Suricata</code>, dan <code>NGINX</code> ke dalam satu skema analisis untuk meningkatkan sensitivitas deteksi terhadap pola serangan spesifik yang mungkin terlewat oleh aturan bawaan. </p>

```xml
<group name="local,syslog,sshd,">
  <rule id="100001" level="5">
  <if_sid>5716</if_sid>
  <srcip>1.1.1.1</srcip>
  <description>sshd: authentication failed from IP 1.1.1.1.</description>
  <group>authentication_failed, pci_dss_10.2.4, pci_dss_10.2.5,</group>
  </rule>
</group>
```

<p align="justify"> &emsp; Bagian ini mendefinisikan <b><i>local custom rule</i></b> untuk mendeteksi anomali autentikasi <code>SSH</code>. Rule ini krusial dalam membuktikan fleksibilitas <code>local rules</code> dalam menangkap insiden umum, seperti kegagalan login dari <code>IP</code> spesifik. </p>

```xml
<group name="ids,suricata,">
  <!-- Severity 1 = highest (e.g. TCP SYN flood, our sid:9000003) -->
  <rule id="86681" level="15">
    <if_sid>86601</if_sid>
    <field name="alert.severity">^1$</field>
    <description>Suricata: Critical Alert - $(alert.signature)</description>
    <group>ddos,</group>
  </rule>

  <!-- Severity 2 = high (e.g. HTTP GET flood, our sid:9000001/9000002) -->
  <rule id="86682" level="10">
    <if_sid>86601</if_sid>
    <field name="alert.severity">^2$</field>
    <description>Suricata: Alert - $(alert.signature)</description>
  </rule>

  <!-- Severity 3 = medium -->
  <rule id="86683" level="5">
    <if_sid>86601</if_sid>
    <field name="alert.severity">^3$</field>
    <description>Suricata: Alert - $(alert.signature)</description>
  </rule>

  <!-- Severity 4 = low -->
  <rule id="86684" level="3">
    <if_sid>86601</if_sid>
    <field name="alert.severity">^4$</field>
    <description>Suricata: Alert - $(alert.signature)</description>
  </rule>

  <!-- Severity not 1-4 -->
  <rule id="86685" level="1">
    <if_sid>86601</if_sid>
    <field name="alert.severity" type="pcre2">^(?![1234]$).*</field>
    <description>Suricata: Alert - $(alert.signature)</description>
  </rule>
</group>
```

<p align="justify"> &emsp; Bagian ini berfungsi dalam mengklasifikasikan alert <code>Suricata</code> berdasarkan tingkat keparahan (<code>severity 1 - 4</code>) agar dapat menentukan prioritas penanganan pada <code>Wazuh</code>. Rule <code>86681</code> hingga <code>86684</code> menyaring peringatan yang bersumber dari rule dasar <code>86601</code> melalui pemeriksaan <code>&lt;field name="alert.severity"&gt;</code>, di mana <code>severity 1</code> (seperti serangan <i>DDoS</i> kritis) diberikan level tertinggi. </p>

```xml
<group name="custom_ddos_rules,suricata,">

  <!-- GoldenEye HTTP flood -->
  <rule id="100200" level="12">
    <if_sid>86600</if_sid>
    <field name="event_type">^alert$</field>
    <match>ET DOS Inbound GoldenEye DoS attack</match>
    <description>HTTP flood (GoldenEye) DoS attack detected by Suricata.</description>
    <mitre><id>T1498</id></mitre>
    <group>ddos,</group>
  </rule>

  <!-- TCP SYN flood -->
  <rule id="100201" level="12">
    <if_sid>86600</if_sid>
    <field name="event_type">^alert$</field>
    <match>SURICATA STREAM 3way handshake SYNACK without ACK</match>
    <description>Possible TCP SYN flood detected on $(srcip).</description>
    <mitre><id>T1498.001</id></mitre>
    <group>ddos,syn_flood,</group>
  </rule>

  <!-- UDP flood -->
  <rule id="100202" level="12">
    <if_sid>86600</if_sid>
    <field name="event_type">^alert$</field>
    <match>ET DOS</match>
    <field name="proto">UDP</field>
    <description>UDP flood DoS pattern detected.</description>
    <mitre><id>T1498.002</id></mitre>
    <group>ddos,udp_flood,</group>
  </rule>

  <!-- Sustained DDoS: 30+ NIDS DoS alerts in 60s -->
  <rule id="100203" level="14" frequency="30" timeframe="60">
    <if_matched_group>ddos</if_matched_group>
    <same_source_ip />
    <description>Active DDoS in progress: >=30 NIDS DoS alerts from $(srcip) in 60s.</description>
    <mitre><id>T1498</id></mitre>
    <group>ddos,active_attack,</group>
  </rule>

  <!-- Layer-7 HTTP flood via NGINX access logs: Rule 31108 fires for 2xx/3xx simple HTTP requests (e.g. AB GET /). 200 such requests from the same source IP in 60s = flood. -->
  <rule id="100204" level="11" frequency="200" timeframe="60">
    <if_matched_sid>31108</if_matched_sid>
    <same_source_ip />
    <description>Layer-7 HTTP flood: 200 requests from $(srcip) in 60s (nginx log).</description>
    <mitre><id>T1498.001</id></mitre>
    <group>web,ddos,</group>
  </rule>

  <!-- Layer-7 HTTP flood detected via Suricata severity-2 alerts: 50 Suricata severity-2 alerts from the same source in 60s = sustained HTTP flood. Custom Suricata local rules (sid:9000001-9000002) fire on request direction, so srcip = attacker (10.0.0.5), enabling correct firewall-drop. -->
  <rule id="100205" level="12" frequency="50" timeframe="60">
    <if_matched_sid>86682</if_matched_sid>
    <same_source_ip />
    <description>HTTP flood detected by Suricata IDS: 50 alerts from $(srcip) in 60s.</description>
    <mitre><id>T1498.001</id></mitre>
    <group>ddos,web,</group>
  </rule>

  <!-- Immediate block on Suricata severity-1 critical alerts (TCP SYN flood, etc.) Custom sid:9000003 fires at priority:1 when SYN flood detected. -->
  <rule id="100208" level="13">
    <if_sid>86681</if_sid>
    <match>ET DOS</match>
    <description>Critical DoS attack detected by Suricata (severity 1): $(alert.signature) from $(srcip)</description>
    <mitre><id>T1498</id></mitre>
    <group>ddos,active_attack,</group>
  </rule>

</group>
```

<p align="justify"> &emsp; Group <code>custom_ddos_rules</code>, <code>suricata</code> membangun deteksi khusus terhadap pola <i>DDoS</i> dari <code>Suricata</code> dan log aplikasi. Rule <code>100200</code> mendeteksi <code>HTTP flood (GoldenEye)</code>, rule <code>100201</code> untuk <code>TCP SYN flood</code>, dan rule <code>100202</code> untuk <code>UDP flood</code>. Ketiga rule ini mengelompokkan trafik ke dalam group <code>ddos</code> untuk korelasi, sehingga <code>Wazuh</code> memahami alert sebagai bagian dari pola serangan besar dengan ancaman tinggi. </p> <p align="justify"> &emsp; Selain itu, rule <code>100203</code> memperkuat korelasi jika muncul <code>30 alert DDoS</code> dalam <code>60 detik</code> dari sumber yang sama, sementara rule <code>100204</code> mendeteksi lonjakan request log <code>NGINX</code> sebagai <code>HTTP flood</code>. Terakhir, rule <code>100205</code> mengakumulasi alert <code>severity 2</code> <code>Suricata</code> menjadi indikasi flood, dan rule <code>100208</code> menjadi pemicu kritis yang menandai <code>severity 1</code> sebagai serangan <code>DoS</code> aktif. </p>

## V: Instalasi Wazuh Agent (VM 2 dan 3)

<p align="justify"> &emsp; Langkah selanjutnya adalah melakukan proses instalasi <code>Wazuh Agent</code> pada <code>VM 2</code> dan <code>VM 3</code>. Di mana langkah implementasinya: </p> <ol> <li> <p align="justify"> <code>SSH</code> ke <code>VM 1</code> menggunakan kredensial yang sudah ditetapkan. </p> </li>
<li>
	<p align="justify">
		Install <code>Wazuh Agent</code>:
	</p>
</li>
</ol>

```sh
sudo apt-get update
sudo apt-get install -y gnupg apt-transport-https

curl -s https://packages.wazuh.com/key/GPG-KEY-WAZUH | sudo gpg --no-default-keyring --keyring gnupg-ring:/usr/share/keyrings/wazuh.gpg --import

sudo chmod 644 /usr/share/keyrings/wazuh.gpg

echo "deb [signed-by=/usr/share/keyrings/wazuh.gpg] https://packages.wazuh.com/4.x/apt/ stable main" | sudo tee /etc/apt/sources.list.d/wazuh.list

sudo apt-get update

sudo WAZUH_MANAGER='[IP Privat Wazuh Manager]' apt-get install -y wazuh-agent

sudo systemctl enable wazuh-agent
sudo systemctl start wazuh-agent
```

<p align="justify"> &emsp; Setelah berhasil dilakukan instalasi, langkah selanjutnya adalah memverifikasi bahwasannya <code>Agent</code> berhasil terdaftar dan terhubung dengan <code>Wazuh Manager</code>. Hal ini dapat dilakukan pada <code>Wazuh Dashboard</code>, dengan memastikan kedua agent berstatus <code>Active</code>. </p> <ol start="3"> <li> <p align="justify"> Mitigasi Isu <b><i>Buffer Overflow</i></b> pada <code>Wazuh Agent</code>: Saat terdeteksi serangan oleh <code>Wazuh</code> dan <code>Suricata</code>, log yang dihasilkan akan berukuran sangat masif yang sesuai dengan jumlah serangan yang dilancarkan. Sehingga, buffer default pada <code>Wazuh Agent</code> akan mengalami <b><i>overflow</i></b>, karena hanya bisa menampung 1024 event. Jika lebih dari itu, agen akan membuang sisa log (<i>silent drop</i>) sehingga <code>Wazuh Manager</code> tidak menerima peringatan apapun. Untuk memperbaikinya, dilakukan konfigurasi bagian <code>/var/ossec/etc/ossec.conf</code> di kedua agent. Cari blok <code>&lt;client_buffer&gt;</code> dan ubah ukurannya menjadi 5000: </p> </li> </ol>

```xml
<client_buffer>
  <disabled>no</disabled>
  <queue_size>5000</queue_size>
  <events_per_second>500</events_per_second>
</client_buffer>
```

<ol start="4"> <li> <p align="justify"> Restart ulang <code>Wazuh Agent</code>: </p> </li> </ol>

```sh
sudo systemctl restart wazuh-agent
```

## VI: Instalasi dan Konfigurasi Suricata dan NGINX (VM 3)

<p align="justify"> &emsp; Pada langkah ini dilakukanlah proses instalasi <code>web server NGINX</code> sebagai target simulasi dan <code>Suricata</code> sebagai sensor keamanan jaringan. </p> <p align="justify"> &emsp; <b>5.1 NGINX dan Suricata</b> </p> <p align="justify"> &emsp; Pada <code>VM 3</code>, install <code>NGINX</code>: </p>

```sh
sudo apt-get install -y nginx
sudo systemctl enable nginx && sudo systemctl start nginx
```

<p align="justify"> &emsp; Langkah selanjutnya adalah melakukan instalasi <code>Suricata</code> melalui repositori <code>PPA</code> resmi untuk memastikan ketersediaan versi terbaru yang telah mendukung mode <code>af-packet</code>: </p>

```sh
sudo add-apt-repository ppa:oisf/suricata-stable -y
sudo apt-get update
sudo apt-get install -y suricata suricata-update

sudo suricata-update
sudo systemctl enable suricata
```

<p align="justify"> &emsp; <b>5.2 Mencegah Banjir Log di suricata.yaml</b> </p> <p align="justify"> &emsp; Secara default, <code>Suricata</code> mencatat setiap koneksi <code>HTTP</code>, <code>TLS</code>, dan <code>DNS</code> ke dalam berkas <code>eve.json</code>. Saat terjadi serangan <i>DDoS</i>, volume log tersebut dapat membengkak drastis sehingga berpotensi membebani penyimpanan. Oleh karena itu, diperlukan optimalisasi agar hanya log bertipe <code>alert</code> yang dicatat. </p> <p align="justify"> &emsp; Implementasi dilakukan menggunakan script <code>Python</code> pada <code>VM 3</code> untuk menonaktifkan pencatatan protokol non-alert di dalam konfigurasi <code>suricata.yaml</code> secara otomatis: </p>

```python
sudo python3 << 'PYEOF'
with open('/etc/suricata/suricata.yaml', 'r') as f:
    lines = f.readlines()

import re

disable_types = {
    'http', 'dns', 'mdns', 'tls',
    'files', 'smtp', 'anomaly', 'dhcp'
}

result = []
i = 0

while i < len(lines):
    line = lines[i]
    m = re.match(r'^(\s+)- (\w[\w-]*)(:)?(\s|$)', line)

    if m and len(m.group(1)) == 8 and m.group(2) in disable_types:
        result.append(line)

        if line.rstrip().endswith(':'):
            result.append('            enabled: no\n')
    else:
        result.append(line)

    i += 1

with open('/etc/suricata/suricata.yaml', 'w') as f:
    f.writelines(result)
PYEOF
```

<p align="justify"> &emsp; Langkah selanjutnya adalah memastikan aktivasi berkas <code>threshold.config</code> dengan melakukan proses <b><i>uncomment</i></b> pada baris <code>threshold-file: /etc/suricata/threshold.config</code> di dalam konfigurasi <code>suricata.yaml</code>. </p>

<p align="justify"> &emsp; <b>5.3 Menulis Rule Deteksi Suricata (Workaround Suricata v8)</b> </p> <p align="justify"> &emsp; Langkah berikutnya adalah menyusun berkas rule kustom pada direktori <code>/var/lib/suricata/rules/local.rules</code>. Perlu diperhatikan adanya kendala kompatibilitas pada <code>Suricata</code> versi 8, di mana fitur <code>detection_filter</code> tidak dapat diintegrasikan bersama fungsi limitasi <code>threshold</code> dalam satu baris rule yang sama, serta kegagalan operasional saat menggunakan protokol <code>alert http</code>. Sebagai solusi alternatif (<b><i>workaround</i></b>), konfigurasi dilakukan dengan menerapkan <code>alert tcp</code> dan memisahkan mekanisme limitasi ke dalam berkas <code>threshold.config</code>: </p>

```sh
sudo tee /var/lib/suricata/rules/local.rules << 'ENDRULES'

# Mendeteksi ApacheBench HTTP Flood
alert tcp any any -> $HOME_NET 80 (msg:"ET DOS ApacheBench HTTP Flood Detected"; content:"ApacheBench"; nocase; detection_filter:track by_src,count 30,seconds 30; priority:2; classtype:web-application-attack; sid:9000001; rev:1;)

# Mendeteksi TCP SYN Flood
alert tcp any any -> $HOME_NET 80 (msg:"ET DOS TCP SYN Flood to HTTP Port"; flags:S,12; detection_filter:track by_src,count 200,seconds 60; priority:1; classtype:attempted-dos; sid:9000003; rev:1;)

ENDRULES
```

<p align="justify"> &emsp; Catatan: </p> <ul> <li> <p align="justify"> Penggunaan arah panah <code>-> $HOME_NET 80</code> bertujuan untuk membatasi observasi <code>Suricata</code> hanya pada trafik yang bersifat inbound. Konfigurasi dua arah berisiko menyebabkan IP server teridentifikasi sebagai sumber ancaman saat mengirimkan paket balasan, yang dapat memicu mekanisme pemblokiran diri sendiri. </p> </li> </ul> <p align="justify"> &emsp; Langkah berikutnya melibatkan penyusunan berkas <code>/etc/suricata/threshold.config</code> untuk melakukan limitasi terhadap alert, dengan menetapkan ambang batas maksimal satu notifikasi per menit untuk setiap entitas IP yang sama. </p>

```sh
sudo tee /etc/suricata/threshold.config << 'EOF'

threshold gen_id 1, sig_id 9000001, type limit, track by_src, count 1, seconds 60
threshold gen_id 1, sig_id 9000003, type limit, track by_src, count 1, seconds 60

EOF
```

<p align="justify"> &emsp; <b>5.4 Memperbaiki Error Socket Tmpfs</b> </p> <p align="justify"> &emsp; Terkadang <code>Suricata</code> gagal start saat server di-reboot karena folder <code>/var/run/suricata/</code> (yang merupakan RAM sementara <code>/tmpfs</code>) terhapus, sehingga user <code>Suricata</code> tidak punya hak akses untuk membuat socket. Kita atasi masalah tersebut dengan mendaftarkannya di <code>systemd-tmpfiles</code>: </p>

```sh
sudo tee /etc/tmpfiles.d/suricata.conf << 'EOF'

d /var/run/suricata 0755 suricata suricata -

EOF
```

<p align="justify"> &emsp; Restart <code>Suricata</code>: </p>

```sh
sudo systemctl restart suricata
```

<p align="justify"> &emsp; Langkah selanjutnya adalah mengonfigurasi <code>VM 3</code> agar mampu melakukan pembacaan terhadap log <code>Suricata</code> dan mengeksekusi instruksi dari <code>Wazuh Manager</code> secara otomatis. Hal ini 22 dilakukan dengan menambahkan blok konfigurasi pemantauan file log pada direktori <code>/var/ossec/etc/ossec.conf</code>, tepat sebelum tag penutup <code>&lt;/ossec_config&gt;</code>: </p>

```xml
<localfile>
  <log_format>json</log_format>
  <location>/var/log/suricata/eve.json</location>
</localfile>

<localfile>
  <log_format>syslog</log_format>
  <location>/var/ossec/logs/active-responses.log</location>
</localfile>
```

## VII: Konfigurasi Pembacaan Logfile (VM 3)

<p align="justify"> &emsp; Tahap selanjutnya melibatkan penyusunan script eksekusi untuk menangani inkonsistensi data. Binary standar <code>Wazuh</code> tidak mampu mengekstrak IP penyerang dari <code>Suricata</code> karena adanya perbedaan format <code>JSON</code>, di mana <code>Suricata</code> menggunakan atribut <code>data.src_ip</code> sementara dekoder bawaan <code>Wazuh</code> mencari <code>data.srcip</code>.
</p>


<p align="justify"> &emsp; Selain itu, terdapat kendala teknis di mana pada daemon <code>wazuh-execd</code> data alert didistribusikan melalui <code>stdin</code> tanpa sinyal <code>EOF</code>, sehingga penggunaan fungsi <code>sys.stdin.read()</code> akan menyebabkan proses tertahan secara permanen. Untuk mengatasi hambatan tersebut, dilakukan pembuatan script <code>Python</code> baru pada direktori <code>/var/ossec/active-response/bin/suricata-firewall-drop</code> dengan menerapkan metode <code>sys.stdin.readline()</code> untuk memastikan pembacaan log berjalan secara interaktif dan otomatis: </p>

```python
#!/usr/bin/env python3

import sys
import json
import subprocess
import datetime

LOG_FILE = "/var/ossec/logs/active-responses.log"

def log(msg):
    ts = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"{ts} active-response/bin/suricata-firewall-drop: {msg}\n")

def get_ip(alert_json):
    data = alert_json.get("parameters", {}).get("alert", {}).get("data", {})
    return (
        data.get("srcip")
        or data.get("src_ip")
        or data.get("flow", {}).get("src_ip", "")
    )

def run_iptables(command, ip):
    flag = "-I" if command == "add" else "-D"
    cmd =

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            log(f"iptables {flag} INPUT -s {ip} -j DROP  [OK]")

        return result.returncode == 0

    except Exception as e:
        log(f"Exception running iptables: {e}")

    return False

def main():
    log("Starting")

    raw = sys.stdin.readline().strip()

    if not raw:
        sys.exit(1)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        sys.exit(1)

    command = data.get("command", "")
    src_ip  = get_ip(data)

    if command in ("add", "delete"):
        run_iptables(command, src_ip)

if __name__ == "__main__":
    main()
```

<p align="justify"> &emsp; Ubah permission-nya agar dapat diakses oleh Wazuh: </p>

```sh
sudo chmod 750 /var/ossec/active-response/bin/suricata-firewall-drop
sudo chown root:wazuh /var/ossec/active-response/bin/suricata-firewall-drop
sudo systemctl restart wazuh-agent
```

## VIII: Instalasi Apache Bench dan Simulasi DDoS (VM 2)

<p align="justify"> &emsp; Langkah selanjutnya adalah melakukan simulasi serangan <i>DDoS</i> terhadap sistem <code>NGINX</code>, dengan harapannya sistem <code>Wazuh</code> dan <code>Suricata</code> mampu mendeteksi serangan tersebut dan melakukan mitigasi secara otomatis. Di mana langkah implementasinya: </p> <ol> <li> <p align="justify"> Pada <code>VM 2</code>, lakukan instalasi <code>Apache Bench</code> yang akan dipakai untuk melakukan simulasi serangan: </p> </li> </ol>

```sh
sudo apt-get install -y apache2-utils
```

<ol start="2"> <li> <p align="justify"> Kemudian lakukan serangan pada situs web <code>NGINX</code> milik <code>VM 3</code>: </p> </li> </ol>

```sh
ab -n 5000 -c 200 -r http://10.0.0.6/
```

<ol start="3"> <li> <p align="justify"> Lakukan Validasi Deteksi Serangan melalui <code>Wazuh Dashboard</code>: </p> </li> </ol> <p align="justify"> &emsp; 27 </p> <p align="justify"> &emsp; 28 </p> <p align="justify"> &emsp; 29 </p> <ol start="4"> <li> <p align="justify"> Lakukan validasi <code>IDS</code> pada file <code>fast.log</code> milik <code>Suricata</code> di <code>VM 3</code>: </p> </li> </ol>

```sh
sudo tail -5 /var/log/suricata/fast.log
```

<ol start="5"> <li> <p align="justify"> Validasi Rule Manager (<code>VM 1</code>) apakah berhasil memvalidasi log dari <code>Suricata</code> dan menjadikannya peringatan kritis: </p> </li> </ol>

```sh
sudo grep -E 'Rule: 100208' /var/ossec/logs/alerts/alerts.log
```

<p align="justify"> &emsp; 30 </p> <ol start="6"> <li> <p align="justify"> Pembuktian <b><i>Active Response</i></b> & Blokir <code>Firewall</code> (<code>VM 3</code>), kembali ke terminal <code>VM 3</code>. Cek log eksekusi <b><i>Active Response</i></b>: </p> </li> </ol>

```sh
sudo cat /var/ossec/logs/active-responses.log
```

<p align="justify"> &emsp; Eksekusi <b><i>active response</i></b> berhasil terekam melalui log <code>iptables -I INPUT -s 10.0.0.5 -j DROP [OK]</code>. Untuk memverifikasi kondisi aktual pada kernel jaringan, jalankan perintah <code>sudo iptables -L INPUT -n</code>, di mana rule <code>DROP</code> akan terlihat terpasang pada prioritas teratas untuk entitas <code>IP 10.0.0.5</code>. </p> <ol start="7"> <li> <p align="justify"> Validasi Pemblokiran Jaringan dilakukan untuk membuktikan efektivitas <code>firewall</code> dalam mengisolasi ancaman. Pengujian dilakukan melalui terminal <code>VM 2</code> dengan mengeksekusi perintah <code>ping -c 5 [IP Privat VM 3]</code>. Hasil pengujian menunjukkan status <code>Operation timed out</code>, yang mengonfirmasi bahwa penyerang telah berhasil diisolasi sepenuhnya dari sistem sasaran. </p> </li> </ol>

## IX: Persiapan Infrastruktur Cloud SOAR di Microsoft Azure

## X: Instalasi Docker dan Shuffle (VM 4)

<p align="justify"> &emsp; Langkah selanjutnya adalah melakukan proses instalasi <b><i>Docker Engine</i></b> pada <code>VM 4</code>. Di mana langkah implementasinya: </p>

```sh
sudo apt remove $(dpkg --get-selections docker.io docker-compose docker-compose-v2 docker-doc podman-docker containerd runc | cut -f1)

sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF

sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl status docker
```

<p align="justify"> &emsp; Setelah proses instalasi selesai, langkah berikutnya adalah melakukan proses instalasi aplikasi <code>Shuffle</code> pada <code>VM 4</code> yang akan dijalankan menggunakan <code>Docker</code>: </p>

```sh
git clone https://github.com/Shuffle/Shuffle
cd Shuffle

sudo chown -R 1000:1000 shuffle-database
sudo swapoff -a
```

<p align="justify"> &emsp; Terakhir, jalankan <code>docker compose</code> di dalam mode <i>background</i> untuk menyalakan Shuffle. </p>

```sh
docker compose up -d
```

## X: Konfigurasi Webhook Wazuh (VM 1)

## XI: Implementasi Workflow Shuffle (VM 4)

## XII: Pembaruan Active Response Wazuh (VM 3)

## XIII: Pengujian Workflow Shuffle

## XIV: Penutup

<p align="justify"> &emsp; Melalui pengaturan logging density dan distribution yang tepat, sistem SIEM Wazuh ini berhasil mendeteksi pola anomali (DDoS) tanpa melumpuhkan infrastruktur Azure yang terbatas. Sistem mampu menyaring trafik yang sangat padat menjadi informasi alert yang ringkas dan mudah dibaca pada dashboard, memastikan fungsionalitas deteksi tetap optimal tanpa membebani sumber daya server.  </p>

THIS IS HOW I WRITE THINGS FOR FUCK SAKE. WHAT PART YOU DONT UNDERSTAND?zure

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

<p align="justify"> &emsp; <code>Wazuh</code> menyediakan script instalasi otomatis yang mempermudah setup <code>Wazuh Indexer</code>, <code>Manager</code>, dan <code>Dashboard</code> dalam satu server sekaligus. Di mana langkah implementasinya: </p> <ol> <li> <p align="justify"> <code>SSH</code> ke <code>VM 1</code> menggunakan kredensial yang sudah ditetapkan. </p> </li>
<li>
	<p align="justify">
		Unduh installer dan aktifkan <code>Wazuh</code>:
	</p>
</li>
</ol>

```sh
# Install Wazuh Manager, Dashboard, dan Indexer
curl -sO https://packages.wazuh.com/4.14/wazuh-install.sh && sudo bash ./wazuh-install.sh -a

# Mengaktifkan Wazuh Manager, Dashboard, dan Indexer
sudo systemctl enable wazuh-manager
sudo systemctl enable wazuh-indexer
sudo systemctl enable wazuh-dashboard

sudo systemctl start wazuh-manager
sudo systemctl start wazuh-indexer
sudo systemctl start wazuh-dashboard
```

<p align="justify"> &emsp; Setelah proses instalasi selesai, <code>Wazuh</code> akan menyediakan kredensial <code>username</code> dan <code>password</code> default yang akan digunakan untuk mengakses <code>Wazuh Dashboard</code> dalam browser. </p>

## IV: Wazuh Custom Rules dan Active Response (VM 1)

<p align="justify"> &emsp; Pada tahap ini dilakukan pengaturan tambahan pada <code>Wazuh</code> agar sistem tidak hanya berfungsi sebagai pusat pemantauan log, tetapi juga mampu melakukan respons otomatis terhadap pola serangan yang terdeteksi. Hal ini dilakukan dengan menerapkan <b><i>active response</i></b> dan <b><i>custom rules</i></b> pada konfigurasi <code>Wazuh Manager</code>. </p> <p align="justify"> &emsp; Langkah pertama adalah melakukan konfigurasi <b><i>active response</i></b> pada file <code>/var/ossec/etc/ossec.conf</code>, dengan konfigurasi pemblokiran umum melalui <code>firewall-drop</code> dan respons jalur khusus untuk alert yang berasal dari <code>Suricata</code>. </p>

```xml
<command>
  <name>suricata-firewall-drop</name>
  <executable>suricata-firewall-drop</executable>
  <timeout_allowed>yes</timeout_allowed>
</command>
```

<p align="justify"> &emsp; Mendefinisikan <b><i>custom command</i></b> pada <code>Wazuh</code> yang nantinya akan dipanggil oleh mekanisme <b><i>active response</i></b> ketika rule tertentu ke trigger. Command <code>suricata-firewall-drop</code> dibuat secara khusus untuk menangani alert yang berasal dari <code>Suricata</code>. </p>

```xml
<active-response>
  <disabled>no</disabled>
  <command>firewall-drop</command>
  <location>local</location>
  <rules_id>5712,5720,5763,100100,100110</rules_id>
  <timeout>1800</timeout>
  <repeated_offenders>30, 60, 120, 180, 240, 360, 720, 1440</repeated_offenders>
</active-response>
```

<p align="justify"> &emsp; Bagian ini mengaktifkan fitur <b><i>active response</i></b> <code>Wazuh</code> untuk memutus koneksi dari pemicu rule spesifik secara otomatis. Pengaturan <code>location local</code> memastikan tindakan dilakukan langsung pada host sumber alert agar pemblokiran lebih relevan. Konfigurasi ini mencakup daftar <code>rules_id</code> pemicu, <code>timeout</code> blokir secara incremental di mulai dari selama 30 menit hingga 1 hari, serta mekanisme <code>repeated_offenders</code> untuk eskalasi durasi bagi penyerang berulang. </p>

```xml
<active-response>
  <disabled>no</disabled>
  <command>suricata-firewall-drop</command>
  <location>local</location>
  <rules_id>86681, 100200, 100201, 100202, 100203, 100204, 100205, 100208</rules_id>
  <timeout>1800</timeout>
  <repeated_offenders>30, 60, 120, 180, 240, 360, 720, 1440</repeated_offenders>
</active-response>
```

<p align="justify"> &emsp; Konfigurasi <b><i>active response</i></b> ini dikhususkan untuk mitigasi <i>DDoS</i> berbasis <code>Suricata</code>. Penggunaan command <code>suricata-firewall-drop</code> diperlukan karena format log <code>JSON NIDS</code> yang berbeda. </p> <p align="justify"> &emsp; Selanjutnya, logika deteksi diperluas melalui <b><i>custom rules</i></b> pada <code>/var/ossec/etc/rules/local_rules.xml</code>. Penambahan ini menyatukan log <code>SSH</code>, <code>Suricata</code>, dan <code>NGINX</code> ke dalam satu skema analisis untuk meningkatkan sensitivitas deteksi terhadap pola serangan spesifik yang mungkin terlewat oleh aturan bawaan. </p>

```xml
<group name="local,syslog,sshd,">
  <rule id="100001" level="5">
  <if_sid>5716</if_sid>
  <srcip>1.1.1.1</srcip>
  <description>sshd: authentication failed from IP 1.1.1.1.</description>
  <group>authentication_failed, pci_dss_10.2.4, pci_dss_10.2.5,</group>
  </rule>
</group>
```

<p align="justify"> &emsp; Bagian ini mendefinisikan <b><i>local custom rule</i></b> untuk mendeteksi anomali autentikasi <code>SSH</code>. Rule ini krusial dalam membuktikan fleksibilitas <code>local rules</code> dalam menangkap insiden umum, seperti kegagalan login dari <code>IP</code> spesifik. </p>

```xml
<group name="ids,suricata,">
  <!-- Severity 1 = highest (e.g. TCP SYN flood, our sid:9000003) -->
  <rule id="86681" level="15">
    <if_sid>86601</if_sid>
    <field name="alert.severity">^1$</field>
    <description>Suricata: Critical Alert - $(alert.signature)</description>
    <group>ddos,</group>
  </rule>

  <!-- Severity 2 = high (e.g. HTTP GET flood, our sid:9000001/9000002) -->
  <rule id="86682" level="10">
    <if_sid>86601</if_sid>
    <field name="alert.severity">^2$</field>
    <description>Suricata: Alert - $(alert.signature)</description>
  </rule>

  <!-- Severity 3 = medium -->
  <rule id="86683" level="5">
    <if_sid>86601</if_sid>
    <field name="alert.severity">^3$</field>
    <description>Suricata: Alert - $(alert.signature)</description>
  </rule>

  <!-- Severity 4 = low -->
  <rule id="86684" level="3">
    <if_sid>86601</if_sid>
    <field name="alert.severity">^4$</field>
    <description>Suricata: Alert - $(alert.signature)</description>
  </rule>

  <!-- Severity not 1-4 -->
  <rule id="86685" level="1">
    <if_sid>86601</if_sid>
    <field name="alert.severity" type="pcre2">^(?![1234]$).*</field>
    <description>Suricata: Alert - $(alert.signature)</description>
  </rule>
</group>
```

<p align="justify"> &emsp; Bagian ini berfungsi dalam mengklasifikasikan alert <code>Suricata</code> berdasarkan tingkat keparahan (<code>severity 1 - 4</code>) agar dapat menentukan prioritas penanganan pada <code>Wazuh</code>. Rule <code>86681</code> hingga <code>86684</code> menyaring peringatan yang bersumber dari rule dasar <code>86601</code> melalui pemeriksaan <code>&lt;field name="alert.severity"&gt;</code>, di mana <code>severity 1</code> (seperti serangan <i>DDoS</i> kritis) diberikan level tertinggi. </p>

```xml
<group name="custom_ddos_rules,suricata,">

  <!-- GoldenEye HTTP flood -->
  <rule id="100200" level="12">
    <if_sid>86600</if_sid>
    <field name="event_type">^alert$</field>
    <match>ET DOS Inbound GoldenEye DoS attack</match>
    <description>HTTP flood (GoldenEye) DoS attack detected by Suricata.</description>
    <mitre><id>T1498</id></mitre>
    <group>ddos,</group>
  </rule>

  <!-- TCP SYN flood -->
  <rule id="100201" level="12">
    <if_sid>86600</if_sid>
    <field name="event_type">^alert$</field>
    <match>SURICATA STREAM 3way handshake SYNACK without ACK</match>
    <description>Possible TCP SYN flood detected on $(srcip).</description>
    <mitre><id>T1498.001</id></mitre>
    <group>ddos,syn_flood,</group>
  </rule>

  <!-- UDP flood -->
  <rule id="100202" level="12">
    <if_sid>86600</if_sid>
    <field name="event_type">^alert$</field>
    <match>ET DOS</match>
    <field name="proto">UDP</field>
    <description>UDP flood DoS pattern detected.</description>
    <mitre><id>T1498.002</id></mitre>
    <group>ddos,udp_flood,</group>
  </rule>

  <!-- Sustained DDoS: 30+ NIDS DoS alerts in 60s -->
  <rule id="100203" level="14" frequency="30" timeframe="60">
    <if_matched_group>ddos</if_matched_group>
    <same_source_ip />
    <description>Active DDoS in progress: >=30 NIDS DoS alerts from $(srcip) in 60s.</description>
    <mitre><id>T1498</id></mitre>
    <group>ddos,active_attack,</group>
  </rule>

  <!-- Layer-7 HTTP flood via NGINX access logs: Rule 31108 fires for 2xx/3xx simple HTTP requests (e.g. AB GET /). 200 such requests from the same source IP in 60s = flood. -->
  <rule id="100204" level="11" frequency="200" timeframe="60">
    <if_matched_sid>31108</if_matched_sid>
    <same_source_ip />
    <description>Layer-7 HTTP flood: 200 requests from $(srcip) in 60s (nginx log).</description>
    <mitre><id>T1498.001</id></mitre>
    <group>web,ddos,</group>
  </rule>

  <!-- Layer-7 HTTP flood detected via Suricata severity-2 alerts: 50 Suricata severity-2 alerts from the same source in 60s = sustained HTTP flood. Custom Suricata local rules (sid:9000001-9000002) fire on request direction, so srcip = attacker (10.0.0.5), enabling correct firewall-drop. -->
  <rule id="100205" level="12" frequency="50" timeframe="60">
    <if_matched_sid>86682</if_matched_sid>
    <same_source_ip />
    <description>HTTP flood detected by Suricata IDS: 50 alerts from $(srcip) in 60s.</description>
    <mitre><id>T1498.001</id></mitre>
    <group>ddos,web,</group>
  </rule>

  <!-- Immediate block on Suricata severity-1 critical alerts (TCP SYN flood, etc.) Custom sid:9000003 fires at priority:1 when SYN flood detected. -->
  <rule id="100208" level="13">
    <if_sid>86681</if_sid>
    <match>ET DOS</match>
    <description>Critical DoS attack detected by Suricata (severity 1): $(alert.signature) from $(srcip)</description>
    <mitre><id>T1498</id></mitre>
    <group>ddos,active_attack,</group>
  </rule>

</group>
```

<p align="justify"> &emsp; Group <code>custom_ddos_rules</code>, <code>suricata</code> membangun deteksi khusus terhadap pola <i>DDoS</i> dari <code>Suricata</code> dan log aplikasi. Rule <code>100200</code> mendeteksi <code>HTTP flood (GoldenEye)</code>, rule <code>100201</code> untuk <code>TCP SYN flood</code>, dan rule <code>100202</code> untuk <code>UDP flood</code>. Ketiga rule ini mengelompokkan trafik ke dalam group <code>ddos</code> untuk korelasi, sehingga <code>Wazuh</code> memahami alert sebagai bagian dari pola serangan besar dengan ancaman tinggi. </p> <p align="justify"> &emsp; Selain itu, rule <code>100203</code> memperkuat korelasi jika muncul <code>30 alert DDoS</code> dalam <code>60 detik</code> dari sumber yang sama, sementara rule <code>100204</code> mendeteksi lonjakan request log <code>NGINX</code> sebagai <code>HTTP flood</code>. Terakhir, rule <code>100205</code> mengakumulasi alert <code>severity 2</code> <code>Suricata</code> menjadi indikasi flood, dan rule <code>100208</code> menjadi pemicu kritis yang menandai <code>severity 1</code> sebagai serangan <code>DoS</code> aktif. </p>

## V: Instalasi Wazuh Agent (VM 2 dan 3)

<p align="justify"> &emsp; Langkah selanjutnya adalah melakukan proses instalasi <code>Wazuh Agent</code> pada <code>VM 2</code> dan <code>VM 3</code>. Di mana langkah implementasinya: </p> <ol> <li> <p align="justify"> <code>SSH</code> ke <code>VM 1</code> menggunakan kredensial yang sudah ditetapkan. </p> </li>
<li>
	<p align="justify">
		Install <code>Wazuh Agent</code>:
	</p>
</li>
</ol>

```sh
sudo apt-get update
sudo apt-get install -y gnupg apt-transport-https

curl -s https://packages.wazuh.com/key/GPG-KEY-WAZUH | sudo gpg --no-default-keyring --keyring gnupg-ring:/usr/share/keyrings/wazuh.gpg --import

sudo chmod 644 /usr/share/keyrings/wazuh.gpg

echo "deb [signed-by=/usr/share/keyrings/wazuh.gpg] https://packages.wazuh.com/4.x/apt/ stable main" | sudo tee /etc/apt/sources.list.d/wazuh.list

sudo apt-get update

sudo WAZUH_MANAGER='[IP Privat Wazuh Manager]' apt-get install -y wazuh-agent

sudo systemctl enable wazuh-agent
sudo systemctl start wazuh-agent
```

<p align="justify"> &emsp; Setelah berhasil dilakukan instalasi, langkah selanjutnya adalah memverifikasi bahwasannya <code>Agent</code> berhasil terdaftar dan terhubung dengan <code>Wazuh Manager</code>. Hal ini dapat dilakukan pada <code>Wazuh Dashboard</code>, dengan memastikan kedua agent berstatus <code>Active</code>. </p> <ol start="3"> <li> <p align="justify"> Mitigasi Isu <b><i>Buffer Overflow</i></b> pada <code>Wazuh Agent</code>: Saat terdeteksi serangan oleh <code>Wazuh</code> dan <code>Suricata</code>, log yang dihasilkan akan berukuran sangat masif yang sesuai dengan jumlah serangan yang dilancarkan. Sehingga, buffer default pada <code>Wazuh Agent</code> akan mengalami <b><i>overflow</i></b>, karena hanya bisa menampung 1024 event. Jika lebih dari itu, agen akan membuang sisa log (<i>silent drop</i>) sehingga <code>Wazuh Manager</code> tidak menerima peringatan apapun. Untuk memperbaikinya, dilakukan konfigurasi bagian <code>/var/ossec/etc/ossec.conf</code> di kedua agent. Cari blok <code>&lt;client_buffer&gt;</code> dan ubah ukurannya menjadi 5000: </p> </li> </ol>

```xml
<client_buffer>
  <disabled>no</disabled>
  <queue_size>5000</queue_size>
  <events_per_second>500</events_per_second>
</client_buffer>
```

<ol start="4"> <li> <p align="justify"> Restart ulang <code>Wazuh Agent</code>: </p> </li> </ol>

```sh
sudo systemctl restart wazuh-agent
```

## VI: Instalasi dan Konfigurasi Suricata dan NGINX (VM 3)

<p align="justify"> &emsp; Pada langkah ini dilakukanlah proses instalasi <code>web server NGINX</code> sebagai target simulasi dan <code>Suricata</code> sebagai sensor keamanan jaringan. </p> <p align="justify"> &emsp; <b>5.1 NGINX dan Suricata</b> </p> <p align="justify"> &emsp; Pada <code>VM 3</code>, install <code>NGINX</code>: </p>

```sh
sudo apt-get install -y nginx
sudo systemctl enable nginx && sudo systemctl start nginx
```

<p align="justify"> &emsp; Langkah selanjutnya adalah melakukan instalasi <code>Suricata</code> melalui repositori <code>PPA</code> resmi untuk memastikan ketersediaan versi terbaru yang telah mendukung mode <code>af-packet</code>: </p>

```sh
sudo add-apt-repository ppa:oisf/suricata-stable -y
sudo apt-get update
sudo apt-get install -y suricata suricata-update

sudo suricata-update
sudo systemctl enable suricata
```

<p align="justify"> &emsp; <b>5.2 Mencegah Banjir Log di suricata.yaml</b> </p> <p align="justify"> &emsp; Secara default, <code>Suricata</code> mencatat setiap koneksi <code>HTTP</code>, <code>TLS</code>, dan <code>DNS</code> ke dalam berkas <code>eve.json</code>. Saat terjadi serangan <i>DDoS</i>, volume log tersebut dapat membengkak drastis sehingga berpotensi membebani penyimpanan. Oleh karena itu, diperlukan optimalisasi agar hanya log bertipe <code>alert</code> yang dicatat. </p> <p align="justify"> &emsp; Implementasi dilakukan menggunakan script <code>Python</code> pada <code>VM 3</code> untuk menonaktifkan pencatatan protokol non-alert di dalam konfigurasi <code>suricata.yaml</code> secara otomatis: </p>

```python
sudo python3 << 'PYEOF'
with open('/etc/suricata/suricata.yaml', 'r') as f:
    lines = f.readlines()

import re

disable_types = {
    'http', 'dns', 'mdns', 'tls',
    'files', 'smtp', 'anomaly', 'dhcp'
}

result = []
i = 0

while i < len(lines):
    line = lines[i]
    m = re.match(r'^(\s+)- (\w[\w-]*)(:)?(\s|$)', line)

    if m and len(m.group(1)) == 8 and m.group(2) in disable_types:
        result.append(line)

        if line.rstrip().endswith(':'):
            result.append('            enabled: no\n')
    else:
        result.append(line)

    i += 1

with open('/etc/suricata/suricata.yaml', 'w') as f:
    f.writelines(result)
PYEOF
```

<p align="justify"> &emsp; Langkah selanjutnya adalah memastikan aktivasi berkas <code>threshold.config</code> dengan melakukan proses <b><i>uncomment</i></b> pada baris <code>threshold-file: /etc/suricata/threshold.config</code> di dalam konfigurasi <code>suricata.yaml</code>. </p>

<p align="justify"> &emsp; <b>5.3 Menulis Rule Deteksi Suricata (Workaround Suricata v8)</b> </p> <p align="justify"> &emsp; Langkah berikutnya adalah menyusun berkas rule kustom pada direktori <code>/var/lib/suricata/rules/local.rules</code>. Perlu diperhatikan adanya kendala kompatibilitas pada <code>Suricata</code> versi 8, di mana fitur <code>detection_filter</code> tidak dapat diintegrasikan bersama fungsi limitasi <code>threshold</code> dalam satu baris rule yang sama, serta kegagalan operasional saat menggunakan protokol <code>alert http</code>. Sebagai solusi alternatif (<b><i>workaround</i></b>), konfigurasi dilakukan dengan menerapkan <code>alert tcp</code> dan memisahkan mekanisme limitasi ke dalam berkas <code>threshold.config</code>: </p>

```sh
sudo tee /var/lib/suricata/rules/local.rules << 'ENDRULES'

# Mendeteksi ApacheBench HTTP Flood
alert tcp any any -> $HOME_NET 80 (msg:"ET DOS ApacheBench HTTP Flood Detected"; content:"ApacheBench"; nocase; detection_filter:track by_src,count 30,seconds 30; priority:2; classtype:web-application-attack; sid:9000001; rev:1;)

# Mendeteksi TCP SYN Flood
alert tcp any any -> $HOME_NET 80 (msg:"ET DOS TCP SYN Flood to HTTP Port"; flags:S,12; detection_filter:track by_src,count 200,seconds 60; priority:1; classtype:attempted-dos; sid:9000003; rev:1;)

ENDRULES
```

<p align="justify"> &emsp; Catatan: </p> <ul> <li> <p align="justify"> Penggunaan arah panah <code>-> $HOME_NET 80</code> bertujuan untuk membatasi observasi <code>Suricata</code> hanya pada trafik yang bersifat inbound. Konfigurasi dua arah berisiko menyebabkan IP server teridentifikasi sebagai sumber ancaman saat mengirimkan paket balasan, yang dapat memicu mekanisme pemblokiran diri sendiri. </p> </li> </ul> <p align="justify"> &emsp; Langkah berikutnya melibatkan penyusunan berkas <code>/etc/suricata/threshold.config</code> untuk melakukan limitasi terhadap alert, dengan menetapkan ambang batas maksimal satu notifikasi per menit untuk setiap entitas IP yang sama. </p>

```sh
sudo tee /etc/suricata/threshold.config << 'EOF'

threshold gen_id 1, sig_id 9000001, type limit, track by_src, count 1, seconds 60
threshold gen_id 1, sig_id 9000003, type limit, track by_src, count 1, seconds 60

EOF
```

<p align="justify"> &emsp; <b>5.4 Memperbaiki Error Socket Tmpfs</b> </p> <p align="justify"> &emsp; Terkadang <code>Suricata</code> gagal start saat server di-reboot karena folder <code>/var/run/suricata/</code> (yang merupakan RAM sementara <code>/tmpfs</code>) terhapus, sehingga user <code>Suricata</code> tidak punya hak akses untuk membuat socket. Kita atasi masalah tersebut dengan mendaftarkannya di <code>systemd-tmpfiles</code>: </p>

```sh
sudo tee /etc/tmpfiles.d/suricata.conf << 'EOF'

d /var/run/suricata 0755 suricata suricata -

EOF
```

<p align="justify"> &emsp; Restart <code>Suricata</code>: </p>

```sh
sudo systemctl restart suricata
```

<p align="justify"> &emsp; Langkah selanjutnya adalah mengonfigurasi <code>VM 3</code> agar mampu melakukan pembacaan terhadap log <code>Suricata</code> dan mengeksekusi instruksi dari <code>Wazuh Manager</code> secara otomatis. Hal ini 22 dilakukan dengan menambahkan blok konfigurasi pemantauan file log pada direktori <code>/var/ossec/etc/ossec.conf</code>, tepat sebelum tag penutup <code>&lt;/ossec_config&gt;</code>: </p>

```xml
<localfile>
  <log_format>json</log_format>
  <location>/var/log/suricata/eve.json</location>
</localfile>

<localfile>
  <log_format>syslog</log_format>
  <location>/var/ossec/logs/active-responses.log</location>
</localfile>
```

## VII: Konfigurasi Pembacaan Logfile (VM 3)

<p align="justify"> &emsp; Tahap selanjutnya melibatkan penyusunan script eksekusi untuk menangani inkonsistensi data. Binary standar <code>Wazuh</code> tidak mampu mengekstrak IP penyerang dari <code>Suricata</code> karena adanya perbedaan format <code>JSON</code>, di mana <code>Suricata</code> menggunakan atribut <code>data.src_ip</code> sementara dekoder bawaan <code>Wazuh</code> mencari <code>data.srcip</code>.
</p>


<p align="justify"> &emsp; Selain itu, terdapat kendala teknis di mana pada daemon <code>wazuh-execd</code> data alert didistribusikan melalui <code>stdin</code> tanpa sinyal <code>EOF</code>, sehingga penggunaan fungsi <code>sys.stdin.read()</code> akan menyebabkan proses tertahan secara permanen. Untuk mengatasi hambatan tersebut, dilakukan pembuatan script <code>Python</code> baru pada direktori <code>/var/ossec/active-response/bin/suricata-firewall-drop</code> dengan menerapkan metode <code>sys.stdin.readline()</code> untuk memastikan pembacaan log berjalan secara interaktif dan otomatis: </p>

```python
#!/usr/bin/env python3

import sys
import json
import subprocess
import datetime

LOG_FILE = "/var/ossec/logs/active-responses.log"

def log(msg):
    ts = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"{ts} active-response/bin/suricata-firewall-drop: {msg}\n")

def get_ip(alert_json):
    data = alert_json.get("parameters", {}).get("alert", {}).get("data", {})
    return (
        data.get("srcip")
        or data.get("src_ip")
        or data.get("flow", {}).get("src_ip", "")
    )

def run_iptables(command, ip):
    flag = "-I" if command == "add" else "-D"
    cmd =

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            log(f"iptables {flag} INPUT -s {ip} -j DROP  [OK]")

        return result.returncode == 0

    except Exception as e:
        log(f"Exception running iptables: {e}")

    return False

def main():
    log("Starting")

    raw = sys.stdin.readline().strip()

    if not raw:
        sys.exit(1)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        sys.exit(1)

    command = data.get("command", "")
    src_ip  = get_ip(data)

    if command in ("add", "delete"):
        run_iptables(command, src_ip)

if __name__ == "__main__":
    main()
```

<p align="justify"> &emsp; Ubah permission-nya agar dapat diakses oleh Wazuh: </p>

```sh
sudo chmod 750 /var/ossec/active-response/bin/suricata-firewall-drop
sudo chown root:wazuh /var/ossec/active-response/bin/suricata-firewall-drop
sudo systemctl restart wazuh-agent
```

## VIII: Instalasi Apache Bench dan Simulasi DDoS (VM 2)

<p align="justify"> &emsp; Langkah selanjutnya adalah melakukan simulasi serangan <i>DDoS</i> terhadap sistem <code>NGINX</code>, dengan harapannya sistem <code>Wazuh</code> dan <code>Suricata</code> mampu mendeteksi serangan tersebut dan melakukan mitigasi secara otomatis. Di mana langkah implementasinya: </p> <ol> <li> <p align="justify"> Pada <code>VM 2</code>, lakukan instalasi <code>Apache Bench</code> yang akan dipakai untuk melakukan simulasi serangan: </p> </li> </ol>

```sh
sudo apt-get install -y apache2-utils
```

<ol start="2"> <li> <p align="justify"> Kemudian lakukan serangan pada situs web <code>NGINX</code> milik <code>VM 3</code>: </p> </li> </ol>

```sh
ab -n 5000 -c 200 -r http://10.0.0.6/
```

<ol start="3"> <li> <p align="justify"> Lakukan Validasi Deteksi Serangan melalui <code>Wazuh Dashboard</code> </p> </li> </ol>  <ol start="4"> <li> <p align="justify"> Lakukan validasi <code>IDS</code> pada file <code>fast.log</code> milik <code>Suricata</code> di <code>VM 3</code>: </p> </li> </ol>

```sh
sudo tail -5 /var/log/suricata/fast.log
```

<ol start="5"> <li> <p align="justify"> Validasi Rule Manager (<code>VM 1</code>) apakah berhasil memvalidasi log dari <code>Suricata</code> dan menjadikannya peringatan kritis: </p> </li> </ol>

```sh
sudo grep -E 'Rule: 100208' /var/ossec/logs/alerts/alerts.log
```

<ol start="6"> <li> <p align="justify"> Pembuktian <b><i>Active Response</i></b> & Blokir <code>Firewall</code> (<code>VM 3</code>), kembali ke terminal <code>VM 3</code>. Cek log eksekusi <b><i>Active Response</i></b>: </p> </li> </ol>

```sh
sudo cat /var/ossec/logs/active-responses.log
```

<p align="justify"> &emsp; Eksekusi <b><i>active response</i></b> berhasil terekam melalui log <code>iptables -I INPUT -s 10.0.0.5 -j DROP [OK]</code>. Untuk memverifikasi kondisi aktual pada kernel jaringan, jalankan perintah <code>sudo iptables -L INPUT -n</code>, di mana rule <code>DROP</code> akan terlihat terpasang pada prioritas teratas untuk entitas <code>IP 10.0.0.5</code>. </p> <ol start="7"> <li> <p align="justify"> Validasi Pemblokiran Jaringan dilakukan untuk membuktikan efektivitas <code>firewall</code> dalam mengisolasi ancaman. Pengujian dilakukan melalui terminal <code>VM 2</code> dengan mengeksekusi perintah <code>ping -c 5 [IP Privat VM 3]</code>. Hasil pengujian menunjukkan status <code>Operation timed out</code>, yang mengonfirmasi bahwa penyerang telah berhasil diisolasi sepenuhnya dari sistem sasaran. </p> </li> </ol>

## IX: Persiapan Infrastruktur Cloud SOAR di Microsoft Azure

<p align="justify"> &emsp; Tahap selanjutnya adalah menyiapkan infrastruktur cloud <b><i>SOAR</i></b> di portal <code>Azure</code>. Di mana langkah pertamanya adalah melakukan navigasi kembali ke <code>Compute Infrastructure → Virtual Machines → Create → Virtual machine</code> untuk membuat <code>Virtual Machine (VM)</code> baru. </p> <p align="justify"> &emsp; Kemudian di halaman <code>Create Virtual Machine</code>, konfigurasikan <code>VM</code> sesuai dengan konfigurasi yang tertera di bawah, dengan catatan <code>VM</code> ditempatkan dalam <code>Resource Group</code> yang sama dengan nama <code>WazuhManager_group</code>. </p> <p align="justify"> &emsp; <b>a. Konfigurasi VM 4 (Shuffle)</b> </p> <ol> <li> <p align="justify"> Di tab <code>Basics</code>, tetapkan <code>resource group</code> yang sama dengan <code>VM Wazuh Manager</code>. </p> </li>
<li>
	<p align="justify">
		Pilih OS <code>Ubuntu Server 24.04 LTS - x64 Gen2</code> dan <code>Size Standard_D2s_v3 (2 vCPU, 8 GiB RAM)</code>.
	</p>
</li>

<li>
	<p align="justify">
		Tetapkan region sebagai <code>(Asia Pacific) East Asia</code> dengan tidak menerapkan redudansi infrastruktur dan keamanan sebagai <code>Standard</code>.
	</p>
</li>

<li>
	<p align="justify">
		Tetapkan hibernasi sebagai mati.
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
		Di tab <code>Networking</code>, buat <code>VNet</code> baru bernama <code>Shuffle-vnet</code> dengan subnet baru sesuai kebutuhan. Untuk <code>VM</code> ini, akan dibuat juga <code>Public IP</code> baru.
	</p>
</li>

<li>
	<p align="justify">
		Klik <code>Review + create</code> dan tunggu proses selesai.
	</p>
</li>
</ol>

## X: Instalasi Docker dan Shuffle (VM 4)

<p align="justify"> &emsp; Langkah selanjutnya adalah melakukan proses instalasi <b><i>Docker Engine</i></b> pada <code>VM 4</code>. Di mana langkah implementasinya: </p>

```sh
sudo apt remove $(dpkg --get-selections docker.io docker-compose docker-compose-v2 docker-doc podman-docker containerd runc | cut -f1)

sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF

sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl status docker
```

<p align="justify"> &emsp; Setelah proses instalasi selesai, langkah berikutnya adalah melakukan proses instalasi aplikasi <code>Shuffle</code> pada <code>VM 4</code> yang akan dijalankan menggunakan <code>Docker</code>: </p>

```sh
git clone https://github.com/Shuffle/Shuffle
cd Shuffle

sudo chown -R 1000:1000 shuffle-database
sudo swapoff -a
```

<p align="justify"> &emsp; Terakhir, jalankan <code>docker compose</code> di dalam mode <i>background</i> untuk menyalakan Shuffle. </p>

```sh
docker compose up -d
```

## X: Konfigurasi Webhook Wazuh (VM 1)

<p align="justify"> &emsp; Langkah selanjutnya adalah melakukan konfigurasi <b><i>webhook</i></b> pada <code>Wazuh</code> dan <code>Shuffle</code> agar keduanya dapat saling terhubung. Di mana langkah implementasinya: </p> <p align="justify"> &emsp; Pada <code>VM 4</code> / <code>Shuffle</code>, lakukan konfigurasi workflow terlebih dahulu: </p> <ol> <li> <p align="justify"> Masuk ke <code>Automate → Workflows</code>. </p> </li>
<li>
	<p align="justify">
		Klik <code>+ Create Workflow</code>.
	</p>
</li>

<li>
	<p align="justify">
		Berikan nama <code>Wazuh</code> kepada workflownya.
	</p>
</li>

<li>
	<p align="justify">
		Tambahkan node <code>Webhook</code> pada bagian <code>Triggers</code>.
	</p>
</li>

<li>
	<p align="justify">
		Ganti nama node tersebut menjadi <code>Wazuh alerts</code>.
	</p>
</li>

<li>
	<p align="justify">
		Klik node tersebut, lalu salin <code>webhook URL</code> yang muncul.
	</p>
</li>

<li>
	<p align="justify">
		Klik <code>Start</code> pada webhook.
	</p>
</li>

<li>
	<p align="justify">
		Klik node <code>Change Me</code>.
	</p>
</li>

<li>
	<p align="justify">
		Ubah <code>action</code> menjadi <code>repeat back to me</code>.
	</p>
</li>

<li>
	<p align="justify">
		Isi <code>Code</code> dengan <code>$exec</code>.
	</p>
</li>

<li>
	<p align="justify">
		Simpan workflow.
	</p>
</li>
</ol> <p align="justify"> &emsp; Setelah itu, pada <code>VM 1</code>, tambahkan blok berikut di dalam <code>&lt;ossec_config&gt;</code> pada file <code>/var/ossec/etc/ossec.conf</code> yang disesuaikan dengan URL yang telah didapatkan pada <code>Shuffle</code>: </p>

```xml
<integration>
  <name>shuffle</name>
  <hook_url>https://shuffler.io/api/v1/hooks/&lt;SHUFFLE_WEBHOOK_ID&gt;</hook_url>
  <alert_format>json</alert_format>
</integration>
```
<p align="justify"> Setelah file disimpan, lakukanlah proses restart terhadap <code>Wazuh Manager</code>: </p>

```sh
sudo systemctl restart wazuh-manager
```

## XI: Implementasi Workflow Shuffle (VM 4)

<p align="justify">
&emsp; Langkah selanjutnya adalah melakukan implementasi workflow pada <code>Shuffle</code> untuk melakukan otomatisasi respons terhadap alert yang dikirimkan oleh <code>Wazuh</code>. Di mana langkah implementasinya:
</p>

<ol type="a">
	<li>
		<p align="justify">
			<code>Webhook</code>, berfungsi untuk menerima alert <code>JSON</code> yang dikirimkan oleh <code>Wazuh</code> sebagai titik masuk utama workflow. Setiap alert yang diterima akan diteruskan ke node berikutnya untuk dilakukan proses analisis dan otomatisasi respons.
		</p>
	</li>
	<li>
		<p align="justify">
			<code>Repeat back to me</code>, pada node <code>Change Me</code>, isi <code>Code</code> dengan <code>$exec</code>. Konfigurasi ini digunakan untuk mengekstrak informasi alert yang dikirimkan oleh <code>Wazuh</code> agar dapat diproses oleh node selanjutnya.
		</p>
	</li>
	<li>
		<p align="justify">
			<code>Shuffle Tools / repeat_back_to_me</code>, digunakan untuk mengekstrak alamat <code>IP</code> dari alert yang diterima. Pada implementasi ini, node berhasil mengembalikan alamat <code>IP</code> penyerang yang nantinya akan digunakan pada proses validasi reputasi dan pemblokiran otomatis.
		</p>
	</li>
	<li>
		<p align="justify">
			<code>AbuseIPDB</code>, gunakan node <code>get_check_ip</code> dan kirim alamat <code>IP</code> hasil ekstraksi dari node sebelumnya. Node ini digunakan untuk memperoleh informasi reputasi alamat <code>IP</code> berdasarkan basis data ancaman milik <code>AbuseIPDB</code>.
		</p>
	</li>
	<li>
		<p align="justify">
			<code>VirusTotal</code>, gunakan node <code>get_an_ip_address_report</code> dan kirim alamat <code>IP</code> yang sama. Informasi yang diperoleh digunakan sebagai sumber validasi tambahan untuk memperkuat proses analisis terhadap alamat <code>IP</code> yang terdeteksi.
		</p>
	</li>
	<li>
		<p align="justify">
			<code>Python decision</code>, isi logic sehingga output menjadi <code>block</code>. Node ini berfungsi sebagai pengambil keputusan yang menentukan tindakan yang akan dikirimkan ke <code>Wazuh</code> berdasarkan hasil analisis dari node-node sebelumnya.
		</p>
	</li>
	<li>
		<p align="justify">
			<code>HTTP Request Get JWT</code>, digunakan untuk melakukan autentikasi terhadap <code>Wazuh API</code>. Node ini akan menghasilkan <code>JSON Web Token (JWT)</code> yang diperlukan untuk mengakses endpoint <code>Wazuh API</code> lainnya.
		</p>
		<ol type="i">
			<li>
				<p align="justify">
					<code>Method</code> : <code>POST</code>
				</p>
			</li>
			<li>
				<p align="justify">
					<code>URL</code> : <code>https://[Wazuh-Public-IP]:55000/security/user/authenticate?raw=true</code>
				</p>
			</li>
			<li>
				<p align="justify">
					<code>Authentication</code> : <code>Basic Auth</code>
				</p>
			</li>
			<li>
				<p align="justify">
					<code>Username</code> : <code>wazuh-wui</code>
				</p>
			</li>
			<li>
				<p align="justify">
					<code>Password</code> : password API yang valid.
				</p>
			</li>
			<li>
				<p align="justify">
					<code>Verify</code> : <code>False</code>
				</p>
			</li>
		</ol>
	</li>
	<li>
		<p align="justify">
			<code>HTTP Request Put Trigger Active Response</code>, digunakan untuk mengirimkan perintah <b><i>active response</i></b> ke <code>Wazuh Agent</code>. Pada implementasi ini, node akan mengirimkan perintah pemblokiran alamat <code>IP</code> yang telah diekstrak sebelumnya melalui <code>Wazuh API</code>.
		</p>
		<ol type="i">
			<li>
				<p align="justify">
					<code>Method</code> : <code>PUT</code>
				</p>
			</li>
			<li>
				<p align="justify">
					<code>URL</code> : <code>https://[Wazuh-Public-IP]:55000/active-response?agents_list=002</code>
				</p>
			</li>
			<li>
				<p align="justify">
					<code>Header</code> : <code>Authorization: Bearer $TOKEN</code>
				</p>
			</li>
			<li>
				<p align="justify">
					<code>Header</code> : <code>Content-Type: application/json</code>
				</p>
			</li>
			<li>
				<p align="justify">
					<code>Body</code> :
				</p>
			</li>
		</ol>
	</li>
</ol>

```json
{
  "command": "!shuffle-firewall-drop",
  "arguments": [
    "$shuffle_tools_1"
  ]
}
```

<p align="justify">
&emsp; Pada implementasi ini, alamat <code>IP</code> dapat diambil langsung dari output node ekstraksi sehingga tidak perlu ditetapkan secara manual. Setelah workflow berhasil dijalankan, request akan menghasilkan respons <code>Wazuh AR command was sent to all agents</code> yang menandakan perintah <b><i>active response</i></b> berhasil dikirimkan ke agent tujuan.
</p>

## XII: Pembaruan Active Response Wazuh (VM 3)

## XIII: Pengujian Workflow Shuffle

## XIV: Penutup

<p align="justify"> &emsp; Melalui pengaturan logging density dan distribution yang tepat, sistem SIEM Wazuh ini berhasil mendeteksi pola anomali (DDoS) tanpa melumpuhkan infrastruktur Azure yang terbatas. Sistem mampu menyaring trafik yang sangat padat menjadi informasi alert yang ringkas dan mudah dibaca pada dashboard, memastikan fungsionalitas deteksi tetap optimal tanpa membebani sumber daya server.  </p>
