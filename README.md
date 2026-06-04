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

## VI: Instalasi dan Konfigurasi Suricata dan NGINX (VM 3)

## VII: Konfigurasi Pembacaan Logfile (VM 3)

## VIII: Instalasi Apache Bench dan Simulasi DDoS (VM 2)

## IX: Instalasi Docker dan Shuffle (VM 4)

## X: Konfigurasi Webhook Wazuh (VM 1)

## XI: Implementasi Workflow Shuffle (VM 4)

## XII: Pembaruan Active Response Wazuh (VM 3)

## XIII: Pengujian Workflow Shuffle

## XIV: Penutup

