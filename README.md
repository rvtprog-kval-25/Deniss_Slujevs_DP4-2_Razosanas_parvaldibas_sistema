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

1. https://flask.palletsprojects.com/
2. https://git-scm.com/doc
3. https://katanamrp.com/
4. https://www.mrpeasy.com/
5. https://www.odoo.com/page/manufacturing
6. https://www.pgadmin.org/docs/
7. https://www.postgresql.org/docs/
8. https://docs.sqlalchemy.org/
9. https://tailwindcss.com/
10. https://vuejs.org/
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

