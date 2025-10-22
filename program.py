from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# === Replace with your Bot Token ===
TOKEN = "8134016932:AAE8VZtf1p6-C2RMV1a3JBeOc_XjbkttFd0"

# Simple quiz questions
QUIZ = [
    {"q": "مين أغشم واحد ف حوت؟", "a": "الشناوي"},
    {"q": "مين شيخك ف حوت؟", "a": "الشيخ عبضو"},
    {"q": "مين اللي جاي من الدييب ويب؟", "a": "أبوعلاء"},
    {"q": "الأوفست؟", "a": "(خيرة(بالتاءالمربوطة"},
    {"q": "こんにちは", "a": "محب"},
    {"q": "خخخخخخخخخخخخخخخخ", "a": "حسن"},
    {"q": "الأدفانسد", "a": "فياض"},
    {"q": "يلا واحد اندومي؟", "a": "فهمسي"}



]

# User state (to track progress)
user_state = {}

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_state[user_id] = {"score": 0, "index": 0}
    await update.message.reply_text("يامرحب بالعضو!\nيلا بينا!")
    await ask_question(update, user_id)

# Function to send questions
async def ask_question(update: Update, user_id):
    index = user_state[user_id]["index"]
    if index < len(QUIZ):
        question = QUIZ[index]["q"]
        await update.message.reply_text(f"Question {index + 1}: {question}")
    else:
        score = user_state[user_id]["score"]
        await update.message.reply_text(f" الاختبار خلص!\nنتيجتك: {score}/{len(QUIZ)}")
        if user_state[user_id]["score"]== len(QUIZ):
            await update.message.reply_text(" انت راجل حوتاوي أصيل")
        else :
            await update.message.reply_text(f"  نتيجة زبالة.انطر بعد اذنك") 
            
        await update.message.reply_text("الكويز انتهى 🎉 اضغط /start لبدء كويز جديد.")
        del user_state[user_id]

# Handle answers
async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_state:
        await update.message.reply_text("اضغط على /start يا فلاح 😄")
        return

    index = user_state[user_id]["index"]
    answer = update.message.text.lower().strip()

    if answer == QUIZ[index]["a"]:
        user_state[user_id]["score"] += 1
        await update.message.reply_text("✅ جدع يلا!")
    else:
        await update.message.reply_text(f"❌ ليه كده يا أصلي : {QUIZ[index]['a'].title()}")

    user_state[user_id]["index"] += 1
    await ask_question(update, user_id)

# Main entry point
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer))

    print("🤖 Quiz bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
