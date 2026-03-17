# ================================================================
#  LIBRARY MANAGEMENT CHATBOT  |  GUI + Terminal  |  Python
#  Axium Library — Smart Replies · Bubble Chat · Smooth Typing
# ================================================================
import datetime, random
import tkinter as tk
from tkinter import scrolledtext

catalog = {
    "B001": {"title": "1984",          "author": "George Orwell", "available": True },
    "B002": {"title": "Clean Code",    "author": "R.C. Martin",   "available": True },
    "B003": {"title": "Harry Potter",  "author": "J.K. Rowling",  "available": False},
    "B004": {"title": "Atomic Habits", "author": "James Clear",   "available": True },
}
members = {"M001": {"name": "Prasad", "borrowed": [], "fine": 0.0}}
loans   = {}
FINE_PER_DAY, LOAN_DAYS = 5.0, 14

INTENTS = {
    "greet":    ["hi", "hello", "hey", "good morning", "good evening", "howdy", "namaste"],
    "list":     ["which books", "what books", "show all", "all books", "available books", "list books", "show books", "books are available"],
    "search":   ["search", "find", "look for", "do you have", "catalog"],
    "borrow":   ["borrow", "issue", "checkout", "lend", "take"],
    "return":   ["return", "give back", "hand in", "drop off"],
    "renew":    ["renew", "extend", "renewal"],
    "reserve":  ["reserve", "hold", "waitlist", "queue"],
    "register": ["register", "join", "enroll", "new member", "sign up"],
    "fine":     ["fine", "penalty", "dues", "outstanding"],
    "inventory":["inventory", "stats", "report", "total books", "how many books", "count"],
    "thanks":   ["thank", "thanks", "great", "awesome", "nice", "perfect", "cool"],
    "bye":      ["bye", "exit", "quit", "goodbye", "see you", "close"],
}
GREETS   = ["Hi! 😊 What book are you looking for today?", "Hello! Great to see you — searching for something specific?", "Hey there! 📚 What can I help you find today?"]
THANKS   = ["You're welcome! 😊 Anything else I can help with?", "Happy to help! Need anything else?", "Always here for you! What else can I do?"]
FALLBACK = ["Hmm, not sure about that! Want me to search for a book or help with borrowing?", "I didn't quite get that — try asking me to find, borrow, or return a book!", "Could you rephrase? I can search books, manage loans, or check fines!"]

def detect(t):
    t = t.lower()
    for intent, kws in INTENTS.items():
        if any(k in t for k in kws): return intent
    return "unknown"

def get_reply(user):
    intent = detect(user);  parts = user.upper().split()
    if intent == "greet":     return random.choice(GREETS)
    if intent == "thanks":    return random.choice(THANKS)
    if intent == "bye":       return "👋 Goodbye! Happy Reading! See you next time 📖"
    if intent == "list":
        avail = [f"  [{i}] {b['title']} by {b['author']}" for i, b in catalog.items() if b["available"]]
        return ("Here are all currently available books:\n" + "\n".join(avail)) if avail else "All books are on loan right now! Try reserving one."
    if intent == "search":
        q = user.lower().split("search")[-1].split("find")[-1].split("look for")[-1].split("do you have")[-1].strip()
        if not q: return "Sure! What title or author are you looking for?"
        r = [f"  [{i}] {b['title']} by {b['author']} — {'✅ Available' if b['available'] else '❌ On Loan'}"
             for i, b in catalog.items() if q in b["title"].lower() or q in b["author"].lower()]
        return ("Here's what I found:\n" + "\n".join(r)) if r else f"No results for '{q}' — try a different keyword!"
    if intent == "borrow":
        isbn = next((t for t in parts if t in catalog), None);  mid = next((t for t in parts if t in members), None)
        if not isbn or not mid: return "To borrow, say:\n  'borrow B001 M001'  (ISBN + Member ID)"
        if not catalog[isbn]["available"]: return f"Oops! '{catalog[isbn]['title']}' is on loan. Want me to reserve it?"
        due = (datetime.date.today() + datetime.timedelta(days=LOAN_DAYS)).isoformat()
        lid = f"L{len(loans)+1:03}"; catalog[isbn]["available"] = False; members[mid]["borrowed"].append(isbn)
        loans[lid] = {"member": mid, "isbn": isbn, "due": due, "returned": False}
        return f"✅ '{catalog[isbn]['title']}' is all yours!\n  📅 Return by: {due}  |  🧾 Loan ID: {lid}"
    if intent == "return":
        isbn = next((t for t in parts if t in catalog), None);  mid = next((t for t in parts if t in members), None)
        if not isbn or not mid: return "To return, say:\n  'return B001 M001'  (ISBN + Member ID)"
        loan = next((l for l in loans.values() if l["member"]==mid and l["isbn"]==isbn and not l["returned"]), None)
        if not loan: return "No active loan found — double-check the ISBN and Member ID!"
        loan["returned"] = True; catalog[isbn]["available"] = True; members[mid]["borrowed"].remove(isbn)
        overdue = max(0, (datetime.date.today() - datetime.date.fromisoformat(loan["due"])).days)
        fine = round(overdue * FINE_PER_DAY, 2)
        if fine: members[mid]["fine"] += fine
        return f"📥 '{catalog[isbn]['title']}' returned!" + (f"\n  ⚠️ Fine: ₹{fine:.2f} for {overdue} overdue days." if fine else "\n  ✅ No fines — right on time!")
    if intent == "renew":
        return "Renewals extend your loan by 14 days!\n  Say: 'return B001 M001' then 'borrow B001 M001'"
    if intent == "reserve":
        isbn = next((t for t in parts if t in catalog), None)
        if not isbn: return "Tell me the ISBN to reserve:\n  'reserve B003 M001'"
        b = catalog.get(isbn)
        return (f"Good news! '{b['title']}' is available — borrow it now!" if b and b["available"] else "🔖 You're on the waitlist! I'll notify you when it's back.")
    if intent == "register":
        p = [x.strip() for x in user.split("|")]
        if len(p) < 2: return "To register:\n  'register | Your Name | email@example.com'"
        mid = f"M{len(members)+1:03}";  members[mid] = {"name": p[1], "borrowed": [], "fine": 0.0}
        return f"🎉 Welcome aboard, {p[1]}!\n  Your Member ID: {mid}. You're ready to borrow books!"
    if intent == "fine":
        mid = next((t.upper() for t in user.split() if t.upper() in members), None)
        if not mid: return "To check fines, say:\n  'fine M001'"
        m = members[mid]
        return f"You're all clear, {m['name']}! No fines 🎉" if m["fine"]==0 else f"💰 {m['name']}, fine: ₹{m['fine']:.2f} — please pay at the counter."
    if intent == "inventory":
        avail = sum(1 for b in catalog.values() if b["available"])
        return f"📊 Library Snapshot:\n  📚 Total: {len(catalog)}  ✅ Available: {avail}  🔄 On Loan: {len(catalog)-avail}\n  👥 Members: {len(members)}"
    return random.choice(FALLBACK)

# ── GUI ──────────────────────────────────────────────────────────
class LibraryBotGUI:
    BG="#0A1628"; SIDE="#071020"; BOT_C="#0E2340"; USER_C="#0F2D1F"; ACC="#38BDF8"; GRN="#4ADE80"

    def __init__(self, root):
        root.title("📚 Axium Library — Assistant"); root.geometry("820x600"); root.configure(bg=self.BG); root.resizable(False, False)
        sb = tk.Frame(root, bg=self.SIDE, width=186); sb.pack(side="left", fill="y"); sb.pack_propagate(False)
        tk.Label(sb, text="📚", font=("Segoe UI Emoji",34), bg=self.SIDE, fg=self.ACC).pack(pady=(26,2))
        tk.Label(sb, text="Library\nAssistant", font=("Georgia",12,"bold"), bg=self.SIDE, fg="white", justify="center").pack()
        tk.Button(sb, text="📋 Show Available Books", font=("Arial",9,"bold"), bg="#0e2a40", fg=self.ACC, bd=0, pady=7, cursor="hand2", activebackground="#163550", command=lambda: self.send_msg("show books")).pack(fill="x", padx=12, pady=(8,4))
        for tip in ["🔍  Search a book","📖  Borrow a book","📥  Return a book","🔖  Reserve a book","👤  Register member","💰  Check fines","📊  Inventory"]:
            tk.Label(sb, text=tip, font=("Arial",9), bg=self.SIDE, fg="#6ab0cc", anchor="w", padx=16).pack(fill="x", pady=2)
        tk.Label(sb, text="© 2025 Axium Library", font=("Arial",7), bg=self.SIDE, fg="#1a3a52").pack(side="bottom", pady=12)
        panel = tk.Frame(root, bg=self.BG); panel.pack(fill="both", expand=True)
        tk.Label(panel, text="  🤖  Hi! I'm your Library Assistant — ask me anything!", font=("Arial",10,"bold"), bg="#060e1a", fg=self.ACC, anchor="w", pady=10, padx=12).pack(fill="x")
        self.chat = scrolledtext.ScrolledText(panel, bg=self.BG, fg="white", font=("Segoe UI",10), bd=0, padx=10, pady=8, state="disabled", wrap="word", cursor="arrow", spacing3=2)
        self.chat.pack(fill="both", expand=True, padx=8, pady=(2,0))
        self.chat.tag_config("bot",      background=self.BOT_C, foreground="#bfdbfe", lmargin1=10, lmargin2=14, rmargin=70, spacing1=4, spacing3=10)
        self.chat.tag_config("user",     background=self.USER_C, foreground="#bbf7d0", lmargin1=70, lmargin2=74, rmargin=10, spacing1=4, spacing3=10)
        self.chat.tag_config("lbl_bot",  foreground=self.ACC, font=("Arial",8,"bold"), lmargin1=10, spacing1=6)
        self.chat.tag_config("lbl_user", foreground=self.GRN, font=("Arial",8,"bold"), lmargin1=70, rmargin=10, spacing1=6)
        self.chat.tag_config("ts",       foreground="#1d3a55", font=("Arial",7), justify="center", spacing1=2, spacing3=1)
        bar = tk.Frame(panel, bg="#050c18", pady=10); bar.pack(fill="x", padx=8, pady=6)
        self.entry = tk.Entry(bar, bg="#0e1f33", fg="white", font=("Segoe UI",11), bd=0, insertbackground=self.ACC, relief="flat")
        self.entry.pack(side="left", fill="x", expand=True, ipady=10, padx=(12,8)); self.entry.bind("<Return>", self.send)
        tk.Button(bar, text="Send ➤", font=("Arial",10,"bold"), bg=self.ACC, fg="#050c18", bd=0, padx=16, pady=8, cursor="hand2", activebackground="#7dd3fc", command=self.send).pack(side="right", padx=(0,12))
        self._animate("Hi there! 👋 Welcome to Axium Library!\nWhat book are you looking for today?"); self.entry.focus()

    def send_msg(self, msg):
        self.entry.delete(0, "end"); self.entry.insert(0, msg); self.send()

    def _push_label(self, tag):
        ts = datetime.datetime.now().strftime("%I:%M %p")
        self.chat.insert("end", f"  {ts}\n", "ts")
        self.chat.insert("end", ("  🤖 Bot\n" if tag=="bot" else "  You\n"), f"lbl_{tag}")

    def _animate(self, text, i=0):
        if i == 0:
            self.chat.config(state="normal"); self._push_label("bot")
            self.chat.insert("end", "  ", "bot"); self.chat.config(state="disabled")
        if i < len(text):
            self.chat.config(state="normal"); self.chat.insert("end", text[i], "bot")
            self.chat.config(state="disabled"); self.chat.see("end")
            self.chat.after(10 if text[i] not in ".!?\n" else 45, lambda: self._animate(text, i+1))
        else:
            self.chat.config(state="normal"); self.chat.insert("end", "\n\n", "bot")
            self.chat.config(state="disabled"); self.chat.see("end")

    def send(self, _=None):
        user = self.entry.get().strip()
        if not user: return
        self.entry.delete(0, "end"); self.chat.config(state="normal")
        self._push_label("user"); self.chat.insert("end", f"  {user}\n\n", "user")
        self.chat.config(state="disabled"); self.chat.see("end")
        reply = get_reply(user)
        self.chat.after(280, lambda: self._animate(reply))
        if detect(user) == "bye": self.chat.after(3500, root.destroy)

if __name__ == "__main__":
    root = tk.Tk()
    try: LibraryBotGUI(root); root.mainloop()
    except KeyboardInterrupt: pass
