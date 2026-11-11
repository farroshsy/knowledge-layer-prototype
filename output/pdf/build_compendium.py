from pathlib import Path
import datetime as dt, json, re, html, textwrap, hashlib
from zoneinfo import ZoneInfo
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether, Preformatted, Flowable
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'output/pdf';NOW=dt.datetime.now(ZoneInfo('Asia/Jakarta'));STAMP=NOW.strftime('%d %B %Y, %H.%M WIB')
FONT=Path('/Users/farros/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/pdfjs-dist/standard_fonts')
for n,f in [('Body','LiberationSans-Regular.ttf'),('Bold','LiberationSans-Bold.ttf'),('Italic','LiberationSans-Italic.ttf')]:pdfmetrics.registerFont(TTFont(n,str(FONT/f)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Italic',boldItalic='Bold')
C=colors.HexColor;TEAL=C('#123E42');MUTED=C('#526568');AMBER=C('#B87920');LINE=C('#D4E1E0')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Text',fontName='Body',fontSize=9.5,leading=14,spaceAfter=7,textColor=C('#26383A'),splitLongWords=True))
styles.add(ParagraphStyle(name='SmallText',parent=styles['Text'],fontSize=8,leading=11,textColor=MUTED))
styles.add(ParagraphStyle(name='Chapter',fontName='Bold',fontSize=21,leading=25,textColor=TEAL,spaceBefore=12,spaceAfter=15,keepWithNext=True))
styles.add(ParagraphStyle(name='Section',fontName='Bold',fontSize=12.5,leading=17,textColor=TEAL,spaceBefore=13,spaceAfter=7,keepWithNext=True))
styles.add(ParagraphStyle(name='Minor',parent=styles['Section'],fontSize=10.5,leading=14,spaceBefore=9))
styles.add(ParagraphStyle(name='BulletText',parent=styles['Text'],leftIndent=12,firstLineIndent=-8,spaceAfter=4))
styles.add(ParagraphStyle(name='QuoteText',parent=styles['Text'],leftIndent=12,borderColor=LINE,borderWidth=1,borderPadding=8,spaceBefore=5,spaceAfter=10))
styles.add(ParagraphStyle(name='CodeText',fontName='Courier',fontSize=7.2,leading=10,textColor=C('#284347'),backColor=C('#F0F5F4'),borderPadding=6,spaceAfter=8))
styles.add(ParagraphStyle(name='TOC0',fontName='Body',fontSize=9.5,leading=14,leftIndent=0,firstLineIndent=0,spaceBefore=7,textColor=TEAL))
styles.add(ParagraphStyle(name='CoverTitle',fontName='Bold',fontSize=37,leading=41,textColor=TEAL,spaceAfter=22))
styles.add(ParagraphStyle(name='CoverSub',fontName='Body',fontSize=16,leading=23,textColor=MUTED,spaceAfter=17))

def norm(s):
 return str(s).replace('\u2011','-').replace('\u2013','-').replace('\u2014',' - ').replace('\u2192',' -> ').replace('\u2260',' != ').replace('\u2264',' <= ').replace('\u2265',' >= ').replace('\u2026','...').replace('\u00a0',' ').replace('&#x20;',' ').replace('\\@','@')
def inline(s):
 s=norm(s);s=html.escape(s)
 s=re.sub(r'\[([^\]]+)\]\((https?://[^\s)]+)\)',lambda m:'<link href="'+m[2]+'" color="#12665E">'+m[1]+'</link>',s)
 s=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',s);s=re.sub(r'`([^`]+)`',r'<font name="Body" color="#196860">\1</font>',s)
 return s
story=[];source_manifest=[]
def p(s,style='Text'):story.append(Paragraph(inline(s),styles[style]))
def chapter(title,source=None,status=None):
 story.append(PageBreak());story.append(Paragraph(inline(title),styles['Chapter']))
 if source:p('Sumber | '+source,'SmallText')
 if status:p('Status bukti | '+status,'SmallText')
def table(headers,rows,widths=None):
 data=[[Paragraph(inline(x),styles['SmallText']) for x in headers]]+[[Paragraph(inline(x),styles['Text']) for x in r] for r in rows]
 t=Table(data,colWidths=widths or [499/len(headers)]*len(headers),repeatRows=1,hAlign='LEFT',splitByRow=1,splitInRow=1)
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),C('#E5EFED')),('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,0),.7,TEAL),('LINEBELOW',(0,1),(-1,-1),.3,LINE)]));story.extend([t,Spacer(1,10)])

class ProcessFlow(Flowable):
 def __init__(self):Flowable.__init__(self);self.width=499;self.height=155
 def draw(self):
  labels=[['INPUT','Business records','Data independen'],['INPUT','Dokumen baru','Sumber tidak tepercaya'],['PROCESS','Ekstraksi & retrieval','Scope, identitas, waktu'],['OUTPUT','Jawaban + evidence','Atau ketidakcukupan']]
  for i,(tag,label,sub) in enumerate(labels):
   x=(i%2)*254;y=85-(i//2)*79
   self.canv.setFillColor(C('#EDF4F2'));self.canv.roundRect(x,y,244,66,6,fill=1,stroke=0);self.canv.setFillColor(TEAL);self.canv.setFont('Bold',8);self.canv.drawString(x+12,y+49,tag);self.canv.setFont('Bold',11);self.canv.drawString(x+12,y+31,label);self.canv.setFont('Body',8);self.canv.drawString(x+12,y+14,sub)
  self.canv.setFont('Body',7);self.canv.setFillColor(MUTED);self.canv.drawString(0,0,'Diagram konseptual target; bukan bukti seluruh kemampuan sudah diimplementasikan.')

class Doc(SimpleDocTemplate):
 def afterFlowable(self,f):
  if isinstance(f,Paragraph) and f.style.name=='Chapter':
   text=f.getPlainText();key='section-'+str(self.seq.nextf('section'));self.canv.bookmarkPage(key);self.canv.addOutlineEntry(text,key,0,False);self.notify('TOCEntry',(0,text,self.page,key))
def footer(c,d):
 c.saveState();w,h=A4
 if d.page>1:
  c.setStrokeColor(LINE);c.line(48,h-35,w-48,h-35);c.setFont('Body',7);c.setFillColor(MUTED);c.drawString(48,h-27,'KNOWLEDGE PLATFORM | RESEARCH, ENGINEERING & DELIVERY');c.line(48,35,w-48,35);c.drawString(48,23,'Snapshot '+NOW.strftime('%d-%m-%Y %H:%M WIB')+' | Bukan klaim production-ready');c.drawRightString(w-48,23,str(d.page))
 c.restoreState()

# Original synthesis: clear reading path before historical source appendices.
story.append(Spacer(1,55));p('KNOWLEDGE PLATFORM','Section');story.append(Spacer(1,12));p('Dari diskusi\nmenjadi sistem yang\nbisa dibuktikan'.replace('\n','<br/>') if False else 'Dari diskusi menjadi sistem yang bisa dibuktikan','CoverTitle');p('Kompendium business process, arsitektur, AI agents, evaluasi, risiko dan keputusan produk','CoverSub');story.append(ProcessFlow());story.append(Spacer(1,25));p('Disusun untuk Farros Hilmi Syafei','Section');p(STAMP,'Text');p('Dokumen rujukan kerja. Fakta, hasil pengujian, usulan, dan keterbatasan diberi konteks secara terpisah. Status aplikasi berubah selama Grok melanjutkan implementasi.','QuoteText')
chapter('Panduan membaca dan batas cakupan')
p('Dokumen ini menggabungkan substansi diskusi yang relevan dengan pembangunan knowledge repository: transisi dari studi kasus AI Interview, brief lanjutan CTO, proses bisnis, penelitian Perkara AI, pilihan stack, model semantik, cara kerja council, evaluasi mikro dan makro, serta hipotesis bisnis. Ini bukan transkrip verbatim setiap pesan.')
p('Bagian utama memberikan sintesis dan cara mengambil keputusan. Lampiran memuat catatan sumber yang lebih panjang, termasuk proposal independen dan kritik. Pengulangan di lampiran dipertahankan bila menunjukkan perbedaan argumen, tetapi teks rendering CSS dan percakapan yang tidak relevan tidak disertakan.')
p('Kredensial, password, private key, informasi kesehatan pribadi, serta instruksi login akun tidak dimasukkan. Materi perusahaan yang belum diberikan tidak diciptakan. Tidak ada data privat CTO yang dipakai untuk mengisi kekosongan.')
table(['Label','Makna'],[['Teramati','Ada sumber kode, event atau hasil eksekusi yang ditautkan. Klaim dibatasi pada sumber/config yang diuji.'],['Laporan penulis','Sumber eksternal menyatakan sesuatu; bukan audit independen.'],['Usulan / hipotesis','Pilihan atau eksperimen yang belum menjadi requirement atau hasil teruji.'],['Belum terukur','Nilai tidak tersedia; bukan nol, bukan gagal otomatis, dan bukan lulus.'],['Historis','Benar untuk snapshot sebelumnya; baca sumber terbaru sebelum menyatakan status sekarang.']],[115,384])
p('Untuk diskusi CTO, baca bagian 1-5, 8-12. Untuk menjalankan pekerjaan, baca bagian 6-10 dan lampiran kontrak. Untuk menilai penelitian, baca lampiran dengan memperhatikan label bukti.','SmallText')
chapter('Daftar isi')
toc=TableOfContents();toc.levelStyles=[styles['TOC0']];story.append(toc)

chapter('1. Konteks, tujuan dan batas tanggung jawab')
p('Studi kasus AI Interview sebelumnya berfokus pada keutuhan assessment dan handoff keputusan manusia. Pelajarannya dibawa ke proyek baru: output AI perlu menjadi pekerjaan yang dapat dipakai, diperiksa dan dipertahankan konsistensinya. Namun repository submission lama dibekukan dan tidak menjadi ruang implementasi baru.')
p('Brief lanjutan CTO meminta sistem lokal yang menghubungkan kumpulan dokumen dengan data terstruktur. Dokumen dummy diizinkan untuk persiapan; pengujian besok dapat memakai dokumen yang baru diberikan. Target checkpoint adalah 11 November 2026 pukul 08.00 WIB.')
p('Ada dua kelas sumber: business records yang berdiri sendiri, dan unstructured documents. Menyimpan hasil ekstraksi dokumen ke tabel tidak otomatis memenuhi syarat dua sumber independen. Pertanyaan harus bisa menggunakan database saja, dokumen saja atau keduanya, dengan batas kemampuan yang dapat dijelaskan.')
p('Horizon enam bulan hanya kemungkinan investasi lanjutan. PoC dapat diteruskan, di-pause, dipivot atau dihentikan. Keberhasilan teknis tidak otomatis membuktikan Proof of Value, product-market fit, readiness produksi atau kontrak pelanggan.')
table(['Keputusan','Pemilik yang tepat'],[['Tujuan bisnis, data nyata, penerimaan risiko','Sponsor/CTO atau pemilik bisnis yang berwenang'],['Domain model dan batas sistem','Engineer dengan review domain dan tim penerima'],['Implementasi slice dan bukti pengujian','Pelaksana/integrator, dibantu worker dan reviewer'],['Usulan AI','Bahan keputusan; tidak menggantikan kewenangan manusia']],[200,299])

chapter('2. Business process sebagai pusat rancangan')
story.append(ProcessFlow());p('User job yang ingin dibantu adalah menyelesaikan pertanyaan operasional dengan evidence yang cukup. Persona awal dan domain resmi Rakamin belum dikonfirmasi; onboarding, peluncuran kelas dan procurement adalah contoh sintetis untuk menguji mekanisme, bukan asumsi proses internal perusahaan.')
for s in ['Pilih notebook/workspace dan pastikan ruang data yang dipakai jelas.','Buat atau impor independent business records dengan stable ID. Nama adalah label, bukan identitas unik.','Masukkan dokumen baru. Nyatakan format/ukuran yang didukung, simpan sumber dan tampilkan keadaan proses.','Klasifikasikan dan ekstrak informasi dengan evidence yang dapat ditemukan kembali. Unknown, mixed atau partial perlu ditampilkan secara proporsional.','Ajukan pertanyaan. Tentukan operasi yang aman, scope dan sumber yang dibutuhkan; ambiguitas tidak boleh menjadi join yang diam-diam.','Kembalikan jawaban beserta records/claims yang mendukung, atau konflik/insufficient evidence. Pengguna dapat membuka sumber.','Simpan hasil dan jalankan ulang setelah restart. Retry tidak menghasilkan duplikasi atau publikasi setengah jadi.']:p('- '+s,'BulletText')
p('Exception flow harus dipikirkan bersama happy path: provider timeout, dokumen tidak terbaca, dua nama sama, sumber bertentangan, input tidak didukung, serta pertanyaan yang tidak memiliki jawaban. Fitur belum memenuhi business process hanya karena satu endpoint mengembalikan HTTP 200.')

chapter('3. Apa yang dipelajari dari Perkara AI')
p('Pengguna memberikan post dan analisis Perkara AI sebagai inspirasi. Pernyataan penulis tentang semantic model, ontology investigasi, multi-layer graph dan event-driven ETL membantu memahami masalah. Itu bukan bukti jenis database, cloud, source code atau benchmark independen mereka.')
p('Pelajaran utamanya adalah mengurangi ambiguitas operasi model melalui representasi pengetahuan yang sesuai domain. Kalimat bahwa seseorang tidak menghadiri rapat tidak boleh diubah menjadi relasi hadir hanya karena nama dan kata meeting muncul bersama. Graph pun dapat menyimpan ekstraksi yang salah; struktur data tidak menghapus kebutuhan validasi.')
p('Satu kumpulan dokumen bisa memuat kategori berbeda. Kategori dokumen, struktur bagian, statement sumber, proposition terstruktur dan finding analitis perlu dibedakan. Sebelas tahapan yang terlihat pada ilustrasi bukan kewajiban sebelas tabel, microservices atau pemeriksaan independen.')
p('Analisis GPT tentang komentar Kevin/Azka dianggap bahan sekunder ketika post aslinya tidak berhasil dibuka langsung. Konsep definitions-versus-instances, semantic views dan governance dapat diperiksa pada dokumentasi primer tanpa mengklaim bahwa implementasi perusahaan komentator sudah diaudit.')
p('Rujukan inti: https://x.com/ibamarief/status/2117104412824944848 ; https://www.w3.org/TR/owl2-primer/ ; https://www.postgresql.org/docs/current/rules-materializedviews.html','SmallText')

chapter('4. Domain model dan invariants')
table(['Konsep','Tanggung jawab / batas'],[['Business record','Data operasional independen dengan stable ID, scope, status dan waktu pencatatan.'],['Source / source version','Sumber asli dan revisinya. Perubahan derivasi tidak boleh menyamar sebagai perubahan sumber.'],['Section / evidence span','Lokasi teks/halaman/waktu yang dapat dibuka. Validitas lokasi terpisah dari dukungan makna.'],['Statement / claim','Apa yang dinyatakan sumber, dengan negasi, modalitas, atribusi dan konteks waktu.'],['Relation / finding','Hubungan atau kesimpulan yang bergantung pada evidence; bukan fakta universal hanya karena dihasilkan model.'],['Query / processing run','Konfigurasi, method, timing, hasil/fallback, dependencies dan status untuk reproduksi.']],[145,354])
p('Invariants yang penting: scope dipaksakan di backend/data path; model tidak mengeksekusi SQL bebas; same-name tidak otomatis same-identity; proposal bukan approval; plan bukan occurrence, tetapi plan saja juga bukan bukti non-occurrence; kesimpulan tidak lebih kuat daripada sumbernya; perubahan ontology atau sumber dapat membuat derivasi lama stale.')
p('Konsep TBox dan ABox berguna untuk membedakan definisi dari instance. Itu tidak mewajibkan OWL engine saat ini. Perubahan definisi dengan dampak luas perlu review manusia dan versi, sedangkan operasi rutin dapat tetap didelegasikan dalam batas yang teruji.')

chapter('5. Stack dipilih dari kebutuhan, bukan popularitas')
p('Prototype baru menggunakan Python, SQLite dan HTML. Repository kasus AI Interview yang diberikan memakai Rails/PostgreSQL/Redis/Sidekiq dan React/TypeScript. Bukti ini hanya berlaku pada repository tersebut; stack seluruh Rakamin dan tim penerima proyek baru belum dipastikan.')
table(['Opsi','Keuntungan potensial','Trade-off / bukti pemicu'],[['Python + SQLite','Reuse kode dan lingkungan lokal; setup kecil; iterasi cepat.','Batas concurrency/operasional dan kontrol produksi tetap perlu dinilai.'],['Python + PostgreSQL','Integritas relasional, MVCC dan jalur pilot multiuser.','Migrasi, driver, provisioning, backup dan ownership menambah pekerjaan.'],['Rails/Postgres + React','Dapat membantu handoff jika benar tim pemilik memakai stack tersebut.','Konfirmasi tim/codebase terlebih dahulu; rewrite malam ini memiliki biaya kesempatan.'],['TypeScript backend','Keselarasan bahasa UI/API dan pengalaman tim tertentu.','Tidak otomatis meningkatkan semantic retrieval atau integritas evidence.'],['Rust untuk hotspot','Ownership dan kontrol memori; kandidat untuk komponen CPU berat yang terukur.','Bukan solusi langsung untuk provider wait, salah join atau claim tidak didukung. Perlu profil dan boundary stabil.']],[110,175,214])
p('Satu ingestion live tercatat timeout 75 detik. Itu mengarahkan perhatian ke provider latency/failure terlebih dahulu; belum ada profil CPU yang membuktikan rewrite bahasa akan menyelesaikan bottleneck. Kinerja, maintainability dan kecepatan delivery perlu diukur pada konteks proyek, bukan diasumsikan dari reputasi bahasa.')

chapter('6. Arsitektur aktual dan opsi evolusi')
p('Boundary logis yang dipertahankan adalah domain, storage, provider, pipeline, HTTP/UI dan evaluation. Modular monolith memungkinkan perubahan terisolasi tanpa membayar koordinasi banyak deployment. Job state tidak otomatis berarti eksekusi asynchronous atau durable queue sudah tersedia.')
p('SQLite cukup untuk menguji alur lokal tertentu, tetapi bukan klaim keamanan multiuser atau skalabilitas enterprise. Materialized views bisa berguna ketika definisi bisnis telah dikurasi; refresh dan freshness tetap harus dikelola. Graph/vector/search projection baru layak ditambahkan jika query nyata menunjukkan kebutuhan yang tidak terselesaikan oleh baseline.')
table(['Alur','Kontrol yang ingin terlihat'],[['Ingestion','Format/size, source hash, status, provider/method, failure/fallback, retry.'],['Extraction','Span exact, attribution, negation/modality; label ketidakpastian.'],['Retrieval','Scope, stable identity, structured operations, coverage dan evidence relevan.'],['Answer','Asersi dibatasi sumber; konflik/ambiguity/abstain dapat diperiksa.'],['Operations','Source/config hash, test evidence, timeout, repeatable start/restart.']],[120,379])
p('Rencana lanjutan bisa mencakup Postgres, object storage, durable jobs, access control dan domain adapters. Ini opsi conditional productization, bukan kemampuan yang dinyatakan telah terimplementasi.')

chapter('7. Retrieval dan penelitian algoritma')
p('Pilihan algoritma sebaiknya mengikuti jenis pertanyaan dan kegagalan baseline. Lexical/exact search penting untuk nama, kode, tanggal dan nominal; semantic retrieval dapat menangani paraphrase; relation traversal membantu pertanyaan multi-hop; semua tetap memerlukan scope dan provenance.')
table(['Referensi','Ide yang layak diuji','Batas pembacaan / adopsi'],[['GraphRAG','Local/global/DRIFT berbeda menurut query scope.','Dokumentasi dibaca; indexing dan global search menambah biaya.'],['LightRAG','Gabungan graph/vector, dua tingkat retrieval dan incremental update.','Paper abstrak/dokumentasi; hasil penulis belum direproduksi lokal.'],['Late Chunking','Konteks embedding dipertahankan sebelum pooling chunk.','Memerlukan embedding pipeline sesuai; bukan menambah prompt jawaban tanpa batas.'],['EAGR, Nov 2026','Ekspansi berbasis evidence pada metadata tanpa graph DB eksplisit.','Preprint baru; maturity dan hasil pada korpus kita belum diketahui.'],['ALCE / ARES','Pisahkan correctness, citation quality, context relevance dan answer support.','Tidak berarti evaluator/benchmark tersebut telah diimplementasikan di sini.']],[95,191,213])
p('Uji satu perubahan terhadap baseline dengan dataset dan budget yang sebanding. Candidate recall, ranking relevance, context size, assertion support, latency dan biaya downstream dapat saling bertentangan. Angka benchmark Perkara AI atau paper tidak boleh dipindahkan menjadi hasil lokal.')

chapter('8. Satu koordinator sebagai brain, banyak worker terbatas')
p('Pengguna sebaiknya berkomunikasi dengan satu koordinator Grok di Orca. Koordinator mengelola task graph, kontrak, ownership file, review, integrasi dan laporan. Worker dapat bekerja paralel pada tugas independen; mereka tidak perlu semuanya terus aktif untuk menghasilkan kemajuan.')
p('Koordinator dipilih untuk penalaran keputusan yang konsekuensial; worker implementasi kecil dapat memakai Build Fast. Saat handoff, Grok 4.7 medium benar-benar diluncurkan. High effort kemudian direkomendasikan, tetapi jangan mengklaim setting sesi sudah berubah tanpa verifikasi. Model lebih kuat tidak menggantikan bukti.')
p('Urutan awal dua proposal -> adjudication -> satu builder -> dua review terbukti terlalu berat untuk sebagian tugas: konteks sekitar 100 ribu karakter dan adjudication 400 detik tercatat. Empat slice kemudian berjalan paralel dengan konteks sekitar 9-39 ribu karakter: query engine, API, UI dan tests. Ini dependency scheduling dengan cache task, bukan sekadar menambah agent.')
p('Aturan kerja: satu owner per file, kontrak dibagi sebelum build, cache berdasarkan input/model/task, integrator tunggal, review atas exact diff, kandidat versioned, fixed tests, dan budget/stop conditions. Jangan menjalankan ulang riset yang sama untuk menyelesaikan bug yang sudah terlokalisasi.')
p('AI council pengembangan berbeda dari runtime council untuk menjawab pertanyaan produk. Keduanya juga berbeda dari governance manusia. Agreement antarmodel dapat berkorelasi; mayoritas tidak membuktikan kebenaran.')

chapter('9. Context memory, graph dan dashboard')
p('Pusat konteks menghubungkan requirement -> business process -> kode -> tests -> risks -> references. MEMORY.md menjadi checkpoint ringkas; state.json dan graph.json menyediakan hubungan yang bisa diambil secara terprogram. Paket sumber menyimpan hash dan nomor baris agar argumen dapat dibaca kembali tanpa menyuntikkan seluruh percakapan berulang kali.')
p('Dashboard aktivitas tersedia di http://127.0.0.1:8766 ketika server lokal hidup. Panel menampilkan call started/finished/failed, waktu event, durasi, model dan artefak. Label running hanya membuktikan call dimulai; proses hidup tidak membuktikan token atau solusi sedang maju. Event yang lama bukan heartbeat provider.')
p('Memory yang diperbarui di disk tidak otomatis masuk ke agent yang sedang menalar. Koordinator perlu menyertakan konteks relevan pada dispatch berikutnya. Saat sesi habis, handoff harus mencatat kandidat, active tasks, hasil gagal, source/config hash, keputusan dan next action. Ingatan model tidak dijadikan satu-satunya system of record.')
p('Proses lokal memerlukan komputer dan Orca tetap menyala. Tidak ada jaminan hosted execution, quota tak terbatas, atau recovery otomatis setelah reboot. STOP global pada supervisor pernah membatalkan audit lain, sehingga penghentian harus scoped dan diperiksa dampaknya.')

chapter('10. Bukti mikro, integrasi, makro dan pengguna nyata')
table(['Tingkat','Yang dapat dibuktikan','Yang belum dapat disimpulkan'],[['Unit/mikro','Kontrak fungsi atau invariant terlokalisasi pada input tertentu.','Alur pengguna lengkap, keamanan menyeluruh atau manfaat bisnis.'],['Integration','Komponen bekerja bersama pada konfigurasi teruji.','Semua format, domain atau query baru didukung.'],['Macro workflow','Perjalanan pengguna selesai dari input sampai evidence/restart.','Utility pengguna nyata atau market fit.'],['Live-model evaluation','Perilaku aktual provider pada kasus/config yang dicatat.','Konsistensi umum dari satu spot check.'],['Pilot/PoV','Pengguna nyata menyelesaikan pekerjaan dengan kualitas/biaya yang diukur.','Tidak otomatis berlaku bagi semua perusahaan/domain.']],[95,205,199])
p('Expected behavior harus ditulis sebelum run. Pisahkan development fixtures, held-out cases, dokumen CTO yang unseen, adversarial cases dan pilot berizin. Jangan mengubah pertanyaan hanya agar test hijau. Ketika protokol evaluator salah, pertahankan raw results dan dokumentasikan koreksi evaluasinya.')
p('Macro v1 memakai tiga contoh sintetis: onboarding, peluncuran kelas dan pengadaan. Hasil awal 6/9: DB-only dan notebook isolation lulus; combined gagal seluruhnya. Ketiga contoh masih satu pola record/memo sehingga bukan tiga bukti independen market fit. Perbaikan sesudahnya harus menunjuk run/hash baru, bukan menghapus baseline gagal.')

chapter('11. Riwayat hasil yang sudah teramati')
table(['Evidence historis','Hasil dan batas'],[['Baseline aplikasi','10 tests lulus; ada ResourceWarning socket HTTP. Bukan angka untuk seluruh produk.'],['Supervisor','13 tests lulus; memeriksa controller/guard, bukan kualitas semantic retrieval.'],['HTTP rules','6/6 pemeriksaan pada protokol terbatas.'],['HTTP live Grok','5/6; ingestion timeout 75s dan fallback rules. Query berikutnya memakai Grok.'],['Integrasi paralel pertama','23 tests: 4 failures, 1 error. Repair berikutnya meloloskan tests, tetapi integrity review menolak kandidat.'],['Macro bisnis awal','6/9 checks; combined route gagal pada tiga workflow sintetis.'],['Repair berikutnya','Ada macro rules 9/9 pada kandidat yang tests/UI-nya masih bermasalah. Bukan penerimaan.'],['Takeover Grok','Koordinator membaca konteks, membuat checkpoint dan meneruskan kandidat terpisah. Status terbaru harus diperiksa langsung.']],[153,346])
p('Tidak boleh menjumlahkan atau membandingkan hitungan ini sebagai satu skor kualitas. Setiap angka memiliki protokol, konfigurasi dan waktu berbeda. Hasil sukses satu layer tidak menghapus kegagalan layer lain. Lampiran snapshot memuat evidence aktual yang dibaca saat PDF dibuat.')
p('Independent review menolak docs-only yang dilabeli db_only, evidence yang melebar ke sibling claims tidak relevan, dan identitas nama substring. Ini contoh mengapa review serta macro test menambah informasi walaupun fixed suite sempat lulus.')

chapter('12. Risiko dan keamanan yang perlu dipertimbangkan')
for s in ['Scope dan authorization: semua retrieval path harus tunduk pada batas workspace; local loopback bukan authentication enterprise.','Input dokumen: ukuran/format, parser versions, filename/content mismatch, source injection dan malicious active content.','Data integrity: transaksi, foreign keys yang benar-benar dideklarasikan, idempotency, retry, stale publication dan version consistency.','Evidence integrity: exact span, active version, semantic support, attribution, numeric accuracy, negation dan temporal event identity.','Provider/process: timeout, descendant cleanup, concurrency/resource limits, fallback label, error propagation dan secrets.','Privacy: lokasi pemrosesan berbeda dari lokasi penyimpanan; dokumen nyata memerlukan keputusan provider/retention yang berwenang.','Supply chain: kemampuan yang diperlukan, maintainer, license, dependency provenance, permissions dan reproducibility sebelum memasang plugin.','Operasional: start/restart, backup/restore, logs yang tidak membocorkan data, limits, support ownership dan monitoring.']:p('- '+s,'BulletText')
p('Kontrol ini adalah kriteria review, bukan pernyataan seluruhnya sudah diterapkan. Panduan OWASP dan NIST membantu menyusun pengujian; membaca panduan tidak memberi sertifikasi. Nol kebocoran pada test finite tidak membuktikan risiko nol.')

chapter('13. Macro value, revenue dan prioritas fitur')
p('Business process dipakai untuk memilih unit nilai yang dapat diamati. Fitur berharga bila membantu pekerjaan yang penting selesai dengan kualitas yang diterima, setelah memperhitungkan waktu review/koreksi dan biaya operasional. Produk yang terlihat cepat tetapi memperbanyak pemeriksaan manual bisa memberi nilai bersih negatif.')
table(['Hipotesis','Unit nilai/revenue potensial','Evidence yang masih dibutuhkan'],[['Internal knowledge','Penghematan operasional; bukan revenue eksternal otomatis.','Task-time baseline, frekuensi penggunaan, correction time.'],['Team workspace','Langganan workspace/seat dengan usage limit.','Buyer, demand, paid pilot dan biaya support.'],['Document/API service','Per document/page/job atau API usage.','Volume, kualitas, unit cost dan kebutuhan integrasi.'],['Private deployment','Lisensi/deployment + maintenance/support.','Kebutuhan data policy, instalasi dan support nyata.'],['Domain package/pilot','Paket workflow khusus atau pilot berbayar.','Problem spesifik, expert review, willingness-to-pay.'],['Integration/onboarding','Scoped project/service fee.','Inventaris sumber dan estimasi delivery; bukan otomatis recurring margin.']],[120,190,189])
p('Rumus kerja yang diusulkan: manfaat operasional bersih dibandingkan dari volume task x selisih waktu yang tervalidasi x biaya tenaga relevan, dikurangi inference, storage, support, maintenance dan implementasi pada horizon yang dinyatakan. Input bisnis tersebut belum tersedia; tidak ada angka ROI atau x-times uplift yang dinyatakan terbukti.')
p('Prioritas: tangani blocker correctness/privacy/security/reproducibility; kemudian workflow yang gagal; kemudian demand/value evidence dan biaya; bandingkan alternatif serta reversibility. Jangan membuat skor ICE/RICE dengan angka demand/effort fiktif. Jangan menjual ulang data pelanggan tanpa hak.')

chapter('14. Delivery, handoff dan keputusan selanjutnya')
p('Koordinator Grok memegang pekerjaan aplikasi; penyusunan PDF ini tidak mengambil alih integrasi atau mengubah kandidat. Kandidat perlu benar-benar dijalankan, diuji dengan input baru, dan ditunjukkan dalam UI. Source asli tetap dipisahkan dari kandidat, dan repository submission lama tetap utuh.')
for s in ['Pilih satu kandidat integrasi dan cek source hash serta latest test/review status. Jangan memakai pointer store-only sebagai final app.','Perbaiki blockers yang teramati dengan slice kecil; re-run test relevan dan macro checks sebelum memperluas fitur.','Jalankan app loopback pada DB dummy terpisah. Buat records independen melalui API/UI; seed dokumen bukan pengganti data bisnis.','Jalankan unseen upload, DB-only/docs-only/combined, ambiguity, insufficient evidence, provider fallback, serta restart.','Verifikasi format yang benar-benar didukung dan browser workflow. HTTP-only tidak membuktikan usability.','Sediakan start command, demo singkat, test evidence dan daftar limitations. Sisakan waktu stabilisasi/rehearsal sebelum 08.00.','Untuk data asli atau investasi lanjutan, konfirmasi persona, data policy, domain expert, team owner dan decision gate continue/pause/pivot.']:p('- '+s,'BulletText')
p('Dua topik masih memerlukan konfirmasi manusia: siapa user/buyer dan domain pertama; serta tim/codebase yang menerima ownership. Tanpa itu, stack alignment dan revenue roadmap tetap usulan, bukan keputusan perusahaan.')

# Snapshot evidence generated without modifying any app source.
chapter('15. Snapshot artefak saat penyusunan PDF')
p('Waktu pengambilan: '+STAMP+'. Hasil baru setelah waktu ini tidak termasuk. Gunakan checkpoint Grok dan dashboard untuk perubahan terbaru.')
for rel in ['council/GROK-TAKEOVER.md','.council-runs/last-run.json','.parallel-builds/latest-reviewed.json']:
 path=ROOT/rel
 p(rel,'Section')
 if path.exists():
  text=path.read_text();source_manifest.append({'path':rel,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'included':'snapshot'})
  if rel.endswith('.json'):p(text[:5000],'SmallText')
  else:
   for line in text.splitlines():
    if line.startswith('#'):p(line.lstrip('# '),'Minor')
    elif line.strip():p(line,'SmallText')
 else:p('File tidak tersedia pada snapshot. Ini bukan bukti acceptance sudah terpenuhi.','SmallText')

# General Markdown renderer: table rows become readable labeled paragraphs to avoid wide-table clipping.
def md(text):
 lines=norm(text).splitlines();i=0;buf=[];code=False;codebuf=[]
 def flush():
  if buf:p(' '.join(buf));buf.clear()
 while i<len(lines):
  line=lines[i];i+=1
  if len(line)>2000 and 'chatgpt-mermaid' in line:continue
  if line.strip().startswith('```'):
   flush()
   if code:
    wrapped=[]
    for ln in codebuf:wrapped.extend(textwrap.wrap(ln,width=94,replace_whitespace=False,drop_whitespace=False) or [''])
    for a in range(0,len(wrapped),35):story.append(Preformatted('\n'.join(wrapped[a:a+35]),styles['CodeText']))
    codebuf=[]
   code=not code;continue
  if code:codebuf.append(line);continue
  if not line.strip():flush();continue
  if re.match(r'^\s*\|',line):
   flush();rows=[line]
   while i<len(lines) and re.match(r'^\s*\|',lines[i]):rows.append(lines[i]);i+=1
   parsed=[[c.strip() for c in r.strip().strip('|').split('|')] for r in rows]
   parsed=[r for r in parsed if not all(re.fullmatch(r'[:\- ]*',c) for c in r)]
   if parsed:
    headers=parsed[0]
    if len(headers)<=4 and len(parsed)<18:
     fixed=[(r+['']*len(headers))[:len(headers)] for r in parsed[1:]]
     try:table(headers,fixed)
     except Exception:
      for r in parsed:p(' | '.join(r),'SmallText')
    else:
     for r in parsed[1:]:p(' ; '.join((headers[j]+': ' if j<len(headers) else '')+v for j,v in enumerate(r)),'SmallText')
   continue
  if re.match(r'^#{1,6}\s',line):flush();p(re.sub(r'^#+\s*','',line),'Section' if line.startswith(('# ','## ')) else 'Minor');continue
  if re.match(r'^\s*([-*]|\d+[.)])\s',line):flush();p(line.strip(),'BulletText');continue
  if line.startswith('>'):flush();p(line.lstrip('> '),'QuoteText');continue
  if re.fullmatch(r'[-=_]{3,}',line.strip()):flush();story.append(Spacer(1,7));continue
  if '[image]' in line and ('favicon' in line or 'google.com/s2' in line):continue
  buf.append(line.strip())
 flush()

appendices=[
('A. Kontrak delivery dan batas scope','DELIVERY.md','Kontrak kerja; bukan bukti fitur selesai.'),
('B. Penjelasan dua sumber independen','council/shared-business-task.md','Panduan brief; domain contoh sintetis.'),
('C. Product foundation versi 0.2','../Research/engineering/submission/screenshots/knowledge-platform-foundation-v0.1 (1).md','Discovery draft eksternal; tidak otomatis menjadi requirement.'),
('D. Proposal business process A','council/business-process-a.md','Proposal Grok independen; belum tentu dipilih/diimplementasikan.'),
('E. Proposal business process B','council/business-process-b.md','Proposal Grok independen; bandingkan dengan A.'),
('F. Risiko dan acceptance awal','research/risk-and-acceptance.md','Historis/usulan; bukan hasil eksekusi semua test.'),
('G. Perkara AI dan semantic model','research/perkara-research.md','Selected-source research; klaim eksternal dibatasi.'),
('H. Counterexamples perilaku publik','research/public-behavior-counterexamples.md','Rancangan falsification; bukan semuanya sudah dijalankan.'),
('I. Referensi lintas domain','research/cross-domain-references.md','Alternatif dan contoh; bukan stack yang sudah dipasang.'),
('J. Pilihan stack dan algoritma','research/stack-and-retrieval-source-notes.md','Catatan primer dan trade-off; hasil paper tidak direproduksi.'),
('K. Review strategi empat perspektif','research/strategy-review-latest.md','Saran model berbasis snapshot historis; bukan otoritas CTO.'),
('L. Review reliability berbasis sumber primer','research/reliability-research-review.md','Saran review; kontrol proposed != implemented.'),
('M. Evaluasi macro dan hipotesis nilai','research/macro-validation-and-value.md','Hasil finite synthetic workflow + ide revenue yang belum divalidasi.'),
('N. Kontrak metrik','docs/metrics-contract.md','Definisi metrik; tidak berarti angka sudah tersedia.'),
('O. Catatan model routing','council/model-routing.md','Routing yang diusulkan/tercatat; cek setting aktif.'),
('P. Draft evaluation cases','council/evaluation-cases-draft.md','Expected cases/dataset draft; bukan test run.'),
('Q. Handoff brainstorming awal','BRAINSTORMING-UPDATE-2026-11-10.md','Snapshot 21.17 WIB; statusnya historis.'),
('R. Rekonstruksi arsitektur GPT',' .context-hub/input-packets/perkara-architecture-review.txt'.strip(),'Analisis sekunder berlabel nomor baris. Detail internal Perkara AI tidak terverifikasi.'),
('S. Analisis thread X dari GPT','.context-hub/input-packets/x-analysis-review.txt','Analisis sekunder; sebagian komentar belum dibuka langsung.'),
]
for title,rel,status in appendices:
 path=(ROOT/rel).resolve()
 if not path.exists():continue
 raw=path.read_text();source_manifest.append({'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'included':'appendix','status':status})
 chapter(title,rel,status)
 if rel.endswith('review.txt'):raw='\n'.join(re.sub(r'^L\d+:\s?','',x) for x in raw.splitlines())
 md(raw)

chapter('Indeks sumber, reproduksi dan pembaruan')
p('Artefak sumber yang disertakan memiliki hash pada source-manifest.json di folder output. PDF ini merupakan snapshot; tidak menggantikan test/review aktual atau approved requirements. Lampiran model dapat mengandung rekomendasi yang saling berbeda. Keputusan terakhir harus direkonsiliasi dengan kontrak dan evidence, bukan dipilih karena gaya bahasanya meyakinkan.')
p('Sumber primer utama','Section')
refs=[('NIST GenAI Profile','https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence'),('OWASP prompt injection','https://genai.owasp.org/llmrisk/llm01-prompt-injection/'),('OWASP file upload','https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html'),('OWASP SQL injection','https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html'),('W3C provenance','https://www.w3.org/TR/prov-overview/'),('W3C OWL primer','https://www.w3.org/TR/owl2-primer/'),('Postgres materialized views','https://www.postgresql.org/docs/current/rules-materializedviews.html'),('SQLite foreign keys','https://www.sqlite.org/foreignkeys.html'),('SQLite WAL','https://www.sqlite.org/wal.html'),('Rust ownership','https://doc.rust-lang.org/book/ch04-01-what-is-ownership.html'),('Python asyncio','https://docs.python.org/3.14/library/asyncio.html'),('GraphRAG','https://microsoft.github.io/graphrag/query/overview/'),('LightRAG','https://arxiv.org/abs/2410.05779'),('Late Chunking','https://arxiv.org/abs/2409.04701'),('EAGR','https://arxiv.org/abs/2611.01910'),('ALCE','https://github.com/princeton-nlp/ALCE'),('ARES','https://aclanthology.org/2024.naacl-long.20/'),('Strategyzer value proposition','https://www.strategyzer.com/library/the-value-proposition-canvas')]
for name,url in refs:p('['+name+']('+url+')','Text')
p('Cara memperbarui','Section');p('Jalankan build_compendium.py memakai runtime Python yang memiliki reportlab/pypdf, lalu render dengan pdftoppm. Periksa halaman, tabel, link, footer dan text extraction. Perbarui bagian sintesis jika keputusan berubah; jangan membiarkan appendices historis menjadi klaim status terbaru.')

pdf=OUT/'Knowledge-Platform-Complete-Discussion-and-Engineering-Compendium.pdf'
doc=Doc(str(pdf),pagesize=A4,rightMargin=48,leftMargin=48,topMargin=49,bottomMargin=49,title='Knowledge Platform - Complete Discussion and Engineering Compendium',author='Prepared for Farros Hilmi Syafei',subject='Business process, architecture, AI coordination, evidence, testing and product decisions')
doc.multiBuild(story,onFirstPage=footer,onLaterPages=footer)
reader=PdfReader(pdf);text='\n'.join(pg.extract_text() or '' for pg in reader.pages)
(OUT/'source-manifest.json').write_text(json.dumps({'generated_at':NOW.isoformat(),'sources':source_manifest,'primary_references':refs},ensure_ascii=False,indent=2));(OUT/'compendium-extracted.txt').write_text(text)
print(json.dumps({'pdf':str(pdf),'pages':len(reader.pages),'text_characters':len(text),'sources':len(source_manifest),'size_bytes':pdf.stat().st_size,'bookmark_count':len(reader.outline)},indent=2))
