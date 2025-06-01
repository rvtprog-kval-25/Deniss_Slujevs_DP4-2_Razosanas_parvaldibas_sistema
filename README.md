# Ražošanas pārvaldības sistēma

Šis projekts ir izstrādāts PIKC “Rīgas Valsts tehnikums” kvalifikācijas darba ietvaros. Tā ir tīmekļa lietotne, kas ļauj uzņēmumiem efektīvāk pārvaldīt ražošanas procesus, pasūtījumus, izejmateriālus un uzdevumus.

Lietotne sastāv no frontend daļas (Vue.js + Tailwind CSS) un backend daļas (Flask + PostgreSQL). Gala rezultāts ir moderna un funkcionāla ražošanas pārvaldības sistēma, ko var izmantot kā prototipu vai pielāgot reālai lietošanai.

---

## 🛠 Izmantotās tehnoloģijas

Projektā izmantotas šādas tehnoloģijas:

- **HTML, CSS (Tailwind CSS)** – lietotāja saskarnes izveidei un dizainam.
- **JavaScript (Vue.js)** – front-end funkcionālitātei.
- **Python (Flask)** – servera daļas loģikai.
- **SQL (PostgreSQL)** – datu glabāšanai.
- **Node.js** – front-end atkarību pārvaldībai un servera palaišanai izstrādes režīmā.
- **SQLAlchemy** – ORM (Object Relational Mapping) starp Python un PostgreSQL.
- **Git** – versiju kontrolei.

---

## 📚 Izmantotie avoti

1. [Flask dokumentācija](https://flask.palletsprojects.com/) – Pallets Projects (apskatīts 10.02.2025)
2. [Git dokumentācija](https://git-scm.com/doc) – Software Freedom Conservancy (apskatīts 29.05.2025)
3. [Katana MRP](https://katanamrp.com/) – Katana Technologies OÜ (apskatīts 15.02.2025)
4. [MRPeasy](https://www.mrpeasy.com/) – MRPeasy (apskatīts 15.02.2025)
5. [Odoo Manufacturing](https://www.odoo.com/page/manufacturing) – Odoo S.A. (apskatīts 15.02.2025)
6. [pgAdmin dokumentācija](https://www.pgadmin.org/docs/) – pgAdmin Dev Team (apskatīts 20.02.2025)
7. [PostgreSQL dokumentācija](https://www.postgresql.org/docs/) – PostgreSQL G.D.G (apskatīts 20.02.2025)
8. [SQLAlchemy dokumentācija](https://docs.sqlalchemy.org/) – SQLAlchemy (apskatīts 25.02.2025)
9. [Tailwind CSS dokumentācija](https://tailwindcss.com/) – Tailwind Labs (apskatīts 23.02.2025)
10. [Vue.js dokumentācija](https://vuejs.org/) – Vue.js (apskatīts 10.02.2025)

---

## 🚀 Uzstādīšanas instrukcija

Lai veiksmīgi palaistu šo projektu uz savas ierīces, jāveic šādas darbības:

### 🔧 1. Priekšnosacījumi

Pirms uzsāc instalēšanu, pārliecinies, ka datorā ir uzinstalēti šie rīki:

- **Python 3.10+**
- **Node.js (18+)**
- **Git**
- **PostgreSQL serveris**
- **Visual Studio Code** (vai cita koda redaktora vide)

---

### 📥 2. Koda lejupielāde

Terminālī vai Git Bash ievadi šādas komandas:
```bash
git clone https://github.com/rvtprog-kval-25/Deniss_Slujevs_DP4-2_Razosanas_parvaldibas_sistema.git
cd Deniss_Slujevs_DP4-2_Razosanas_parvaldibas_sistema

🐍 3. Backend (Flask) instalēšana
cd kv.darbsbackend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

🔐 4. Vides konfigurācija
Tajā pašā kv.darbsbackend mapē izveido failu ar nosaukumu .env un pievieno šādu saturu:
DATABASE_URL=postgresql://postgres.dlsjcbkiordnguoewjol:Monkins2707@aws-0-eu-north-1.pooler.supabase.com:6543/postgres
SECRET_KEY=supersecretkey123

▶️ 5. Backend servera palaišana
python index.py
  
🌐 6. Frontend (Vue.js) uzstādīšana
Atgriezies atpakaļ uz projekta saknes mapi:
cd ..

Instalē front-end atkarības:
npm install

Palaid front-end serveri:
npm run dev

