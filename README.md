# 📚 Library Management – Extended Version by Menna Reda

This Odoo module enhances the base **Library Management System** with robust borrowing workflows, reporting, dashboards, and a cleaner user experience.

---

## 🚀 Features Overview

### 📘 Books
- Title, Author (new model), ISBN (validated), Publication Year
- `total_copies` and computed `available_copies`
- Auto-updated `status`: **Available** or **Borrowed**
- **Kanban view** added for quick browsing

### ✍️ Authors
- New `library.author` model with Tree and Form views

### 🔁 Loans
- `borrow_date` and computed `return_date` (+14 days)
- Smart `status`: `draft`, `borrowed`, `returned`, `overdue`
- `loan_line_ids`: supports multiple books per loan

### 📌 Loan Lines
- Each line has its own `status`: `active`, `returned`, `overdue`
- Borrowing is **blocked** when no copies are available
- Editable inline in the loan form

---

## 🎨 Usability Enhancements

- **Kanban View for Books**  
  Clean card layout with title, author, availability, and status.

- **Smart Buttons**
  - On `res.user`: View member’s loan history
  - On `library.loan`: Return all books, Reset to Draft (manager-only)

- **Status Override Field**
  - Allows manual transition via buttons without breaking computed logic

---

## 📈 Dashboard & Reporting

### 🔝 Top 3 Borrowed Books – Graph View
- SQL view `library_book_stats` groups loan lines by book
- Counts borrow frequency and returns only **top 3**
- Displayed as a **bar chart** in Dashboard → Reports

### ⚠️ Overdue Loans – Graph View
- Filters loans overdue by return date
- Shown under Configuration → Dashboard

### 🧾 PDF Report: Borrowed Books
- QWeb report listing member, book title, borrow date, status
- Accessible from **Reports menu**
- Supports multi-select printing from Loans view
  
---

## 🕒 Automation

- ✅ **Automated Cron Job**: Checks daily for overdue loans
- ✅ Updates loan and loan line `status` to `"overdue"`
- ✅ Sends **email reminders** using a QWeb email template

---

## 🔒 Data Integrity

- ISBN must be exactly 13 digits
- Borrowing disallowed when `available_copies <= 0`
- `available_copies` is computed based on real-time loan lines
- `status` is computed but can be overridden via buttons

---

## ⚙️ Technical Highlights

- Custom SQL view with `MIN(id)` for ORM compatibility
- Model: `library.book.stats` is `_auto = False` and readonly
- Uses proper `@api.depends`, `@api.constrains`, and separation of concerns
- Buttons: `Confirm Borrow`, `Return All`, `Reset to Draft` with proper role permissions

---

## ✅ What I Added:

- ✅ **Author model** with full views
- ✅ **Kanban view** for books
- ✅ **Smart borrowing logic** with availability check
- ✅ **Top 3 borrowed books graph** using real SQL view
- ✅ **PDF report** for borrowed books

---

## 👩‍💻 Author

**Menna Reda**  

---

