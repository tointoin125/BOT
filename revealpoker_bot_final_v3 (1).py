#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "7564608520:AAF8cpTz9lqDN8GGK3E0xkCy8Q7gX9QCMSw"  # User's provided token
WEBSITE_URL = "https://www.revealpoker.top"
INSTAGRAM_URL = "https://www.instagram.com/hackpoker_updated/"
ADMIN_TELEGRAM_URL = "https://t.me/bedmalcon_temp" # Updated admin link

# --- Helper function to escape MarkdownV2 special characters ---
def escape_markdown_v2(text):
    # Escape all special characters listed in Telegram Bot API documentation for MarkdownV2
    # Characters: _, *, [, ], (, ), ~, `, >, #, +, -, =, |, {, }, ., !
    escape_chars = r"[_*[\]()~`>#+\-=|{}.!]"
    return re.sub(escape_chars, r"\\\1", text)

# --- Text and Button Definitions (from conversation_flow_design_en_markdown_v2.md) ---
# All texts are now pre-escaped for MarkdownV2 where necessary, or will be escaped by the escape_markdown_v2 function.
# For simplicity in defining them here, we will apply escape_markdown_v2() before sending.
# However, for texts that *already contain* valid MarkdownV2 (like *bold* or _italic_), 
# we must be careful not to double-escape or to manually craft them.
# The design doc `conversation_flow_design_en_markdown_v2.md` has them pre-escaped.
# We will use those directly.

WELCOME_MESSAGE = (
    "🤫 Hey there, future poker master\! A warm welcome to the *RevealApp Bot*, your personal agent to unlock an _unbeatable_ edge at the tables\! 🃏\n\n"
    "With RevealApp, you don\'t just play, you *dominate*, anticipating your opponents\' every move\. No more guesswork; it\'s time to transform your game\!\n\n"
    "To start your journey to victory, on which platform are you seeking this secret advantage? Choose below: 👇"
)

PLATFORM_BUTTONS_CONFIG = [
    [{"text": "♣️ ClubGG", "callback_data": "platform_clubgg"}],
    [{"text": "♠️ XPoker", "callback_data": "platform_xpoker"}],
    [{"text": "♦️ PPPoker", "callback_data": "platform_pppoker"}],
]

# --- Helper function to build keyboards ---
def build_keyboard(buttons_config):
    keyboard = []
    for row_config in buttons_config:
        row = []
        for button_item in row_config:
            if 'url' in button_item:
                row.append(InlineKeyboardButton(button_item['text'], url=button_item['url']))
            else:
                row.append(InlineKeyboardButton(button_item['text'], callback_data=button_item['callback_data']))
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)

# --- Command Handlers & Callback Query Handlers ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_markup = build_keyboard(PLATFORM_BUTTONS_CONFIG)
    if update.message:
        await update.message.reply_text(WELCOME_MESSAGE, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)
    elif update.callback_query:
        # Ensure the message is edited if it's a callback query
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(WELCOME_MESSAGE, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)

async def handle_platform_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    platform_choice = query.data
    context.user_data['platform'] = platform_choice

    platform_name = ""
    channel_url = ""
    # callback_prefix = platform_choice.split('_')[1]

    if platform_choice == 'platform_clubgg':
        platform_name = "ClubGG"
        channel_url = 'https://t.me/clubggcheat'
        message_text = (
            f"Excellent choice\! 🚀 With RevealApp for *{platform_name}*, you\'ll have access to your opponents\' cards, "
            f"turning every hand into a golden opportunity\! Imagine the confidence of knowing exactly where you stand\.\n\n"
            f"What would you like to do now?"
        )
    elif platform_choice == 'platform_xpoker':
        platform_name = "XPoker"
        channel_url = 'https://t.me/+-zchdfB3z-ZmYTQx'
        message_text = (
            f"Great decision\! 🔥 RevealApp for *{platform_name}* is your secret weapon to decipher your adversaries and make "
            f"decisions with surgical precision\. Get ready to see the game in a whole new way\!\n\n"
            f"What\'s your next step?"
        )
    elif platform_choice == 'platform_pppoker':
        platform_name = "PPPoker"
        channel_url = 'https://t.me/crackpppokerhack'
        message_text = (
            f"Champion\'s choice\! 🏆 With RevealApp for *{platform_name}*, your opponents\' cards will no longer be a mystery\. "
            f"Play with the peace of mind of someone who\'s always one step ahead\!\n\n"
            f"What do you want to explore?"
        )
    else:
        await query.edit_message_text(text="Invalid selection\. Please try again\.", parse_mode=ParseMode.MARKDOWN_V2)
        return

    keyboard_config = [
        [{'text': f"📢 Join {platform_name} Channel", 'url': channel_url}],
        [{'text': "💰 How to Buy RevealApp", 'callback_data': f'how_to_buy_generic'}],
        [{'text': "✨ See All Advantages", 'callback_data': f'features_generic'}],
        [{'text': "🔙 Back to Platforms", 'callback_data': 'start_over'}]
    ]
    reply_markup = build_keyboard(keyboard_config)
    await query.edit_message_text(text=message_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)

async def handle_how_to_buy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    message_part1 = (
        "You\'re one step away from revolutionizing your game\! 🚀 Acquiring *RevealApp* is simple, and the return is _immeasurable_\.\n\n"
        "*Why is RevealApp your best investment?*\n"
        "\- 👁️ *Total Vision:* Know your opponents\' cards\. _Yes, that\'s right\!_\n"
        "\- 📈 *Profitable Decisions:* No more uncertain bluffs or doubtful calls\. Play with privileged information\.\n"
        "\- 🛡️ *Secure and Undetectable:* Our advanced technology ensures your advantage discreetly and safely\.\n"
        "\- 📱 *Multi\-platform:* Works perfectly on Android and iOS for the platforms you love\.\n\n"
        "Ready for the next level? See how easy it is to get yours:"
    )
    await query.edit_message_text(text=message_part1, parse_mode=ParseMode.MARKDOWN_V2)

    message_part2 = (
        "*How to Buy and Activate RevealApp in Minutes:*\n\n"
        "1️⃣ *Access Our Official Website:*\n"
        f"   Click the button below or visit [www\.revealpoker\.top]({WEBSITE_URL})\n"
        "   _That\'s where the magic happens\! ✨_\n\n"
        "2️⃣ *Choose Your Ideal Plan:*\n"
        "   We have options for all types of players, from the casual enthusiast to the dedicated professional\. Find what _best suits_ your ambition\!\n\n"
        "3️⃣ *Provide Your Device Information \(IMEI\):*\n"
        "   For secure and personalized activation, we\'ll need your device\'s IMEI\. _Rest assured, this information is stored locally on your device for your privacy and convenience\._\n\n"
        "4️⃣ *Activate and Dominate\!*\n"
        "   Follow the simple instructions on our website to activate the app\. In moments, you\'ll be seeing poker in a way you never imagined\!\n\n"
        "*Don\'t waste any more time and money on guesswork\!* Every hand you play without RevealApp is a missed earning opportunity\."
    )
    
    keyboard_config = [
        [{'text': "🛒 GO TO REVEALPOKER.TOP AND BUY NOW!", 'url': WEBSITE_URL}],
        [{'text': "🌟 See Detailed Plans & Pricing (on website)", 'url': WEBSITE_URL}],
        [{'text': "🤔 Still have questions... (FAQ)", 'callback_data': 'faq'}],
        [{'text': "💬 Talk to Support / Contact Admin", 'callback_data': 'contact_support'}],
        [{'text': "🔙 Back to Previous Menu", 'callback_data': context.user_data.get('platform', 'start_over')}]
    ]
    reply_markup = build_keyboard(keyboard_config)
    await query.message.reply_text(text=message_part2, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)

async def handle_features(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    message_text = (
        "🃏 *Unlock Your Ultimate Advantage with RevealApp\!* 🃏\n\n"
        "Curious about what makes RevealApp a game\-changer? Brace yourself:\n\n"
        "1\.  🌟 *Unprecedented Insight:* Imagine knowing your opponents\' cards in PPPOKER, XPoker & ClubGG\. _This isn\'t a dream; it\'s RevealApp\!_ Make informed decisions, stop guessing, and start winning like never before\!\n\n"
        "2\.  📱 *Flawless Multi\-Platform Support:* Whether on Android or iOS, RevealApp works seamlessly with PPPOKER, XPoker, and ClubGG\. Your winning edge, on your preferred device\.\n\n"
        "3\.  🛡️ *Secure & Totally Undetectable:* Worried about prying eyes? _Don\'t be\._ Our cutting\-edge technology ensures your advantage remains your secret\. Play with confidence, knowing you\'re one step ahead, discreetly\.\n\n"
        "RevealApp isn\'t just an app; it\'s your key to consistency and bigger profits in online poker\. Thousands of players are already transforming their game\. _Will you be next?_\n\n"
        "*What would you like to do?*"
    )
    keyboard_config = [
        [{'text': "💰 How to Buy Now!", 'callback_data': 'how_to_buy_generic'}],
        [{'text': "🗣️ See Testimonials from Users", 'callback_data': 'testimonials'}],
        [{'text': "📜 Learn Our Story", 'callback_data': 'story'}],
        [{'text': "🔙 Back to Previous Menu", 'callback_data': context.user_data.get('platform', 'start_over')}]
    ]
    reply_markup = build_keyboard(keyboard_config)
    await query.edit_message_text(text=message_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)

async def handle_faq(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    faq_text = (
        "*Frequently Asked Questions \(FAQ\)* 🤔\n\n"
        "*Q1: Is RevealApp safe to use? Will I get banned?*\n"
        "A: We prioritize your security\. RevealApp uses advanced, discreet technology designed to be undetectable\. While no tool can offer a 100% lifetime guarantee against all future detection methods by game platforms, our users have been enjoying the benefits securely\. We constantly update our app to stay ahead\. _Play smart, play discreetly\._\n\n"
        "*Q2: How does the IMEI activation work? Is my data safe?*\n"
        "A: The IMEI is used for a one\-time secure activation tied to your device\. This information is processed securely and is primarily for licensing purposes, stored locally on your device\. We respect your privacy\.\n\n"
        "*Q3: What if the app stops working or a game platform updates?*\n"
        "A: Your subscription includes updates to ensure compatibility with supported platforms \(ClubGG, XPoker, PPPoker\) and to address any changes\. Our team works diligently to keep RevealApp effective\.\n\n"
        "*Q4: Can I use one license on multiple devices?*\n"
        "A: Typically, a license is tied to a single device via IMEI for security and to prevent abuse\. Please check the specific terms of your chosen plan on our website\.\n\n"
        "Have more questions? Our team is ready to help\!"
    )
    keyboard_config = [
        [{'text': "✅ Got it! I Want to Buy!", 'callback_data': 'how_to_buy_generic'}],
        [{'text': "💬 Talk to Admin (Telegram)", 'url': ADMIN_TELEGRAM_URL}],
        [{'text': "📸 Check our Instagram", 'url': INSTAGRAM_URL}],
        [{'text': f"🌐 Visit {escape_markdown_v2(WEBSITE_URL.replace('https://', ''))}", 'url': WEBSITE_URL}],
        [{'text': "🔙 Back to Previous Menu", 'callback_data': context.user_data.get('platform', 'start_over')}]
    ]
    reply_markup = build_keyboard(keyboard_config)
    await query.edit_message_text(text=faq_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)

async def handle_contact_support(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    contact_text = (
        "*Get in Touch with RevealApp Support & Admin* 💬\n\n"
        "Have questions, need assistance, or just want to know more before you dominate the tables? Here’s how you can reach us:\n\n"
        "\- *Direct Admin Contact \(Telegram\):* For urgent queries or direct chat\. \(Link below\)\n"
        "\- *Our Website:* For comprehensive information, FAQs, and official contact channels\.\n"
        "\- *Instagram:* Stay updated with our latest news and community\!\n\n"
        "_Your winning journey is important to us\! Choose your preferred way to connect below\._"
    )
    keyboard_config = [
        [{'text': "👨‍💻 Talk to Admin (Telegram)", 'url': ADMIN_TELEGRAM_URL}],
        [{'text': "📸 Visit our Instagram", 'url': INSTAGRAM_URL}],
        [{'text': f"🌐 Visit {escape_markdown_v2(WEBSITE_URL.replace('https://', ''))} for Info & Purchase", 'url': WEBSITE_URL}],
        [{'text': "💰 I\'m Ready to Buy Now!", 'callback_data': 'how_to_buy_generic'}],
        [{'text': "🔙 Back to Previous Menu", 'callback_data': context.user_data.get('platform', 'start_over')}]
    ]
    reply_markup = build_keyboard(keyboard_config)
    await query.edit_message_text(text=contact_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)

async def handle_story(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    story_text = (
        "📜 *Our Story: How We Revolutionized Poker* 📜\n\n"
        "Ever felt like the odds were unfairly stacked against you? That\'s exactly how our journey began\. A series of unexpected, almost unbelievable, defeats in online poker sparked a deep dive\. We were determined to understand if there was more to these games than met the eye\.\n\n"
        "Months of rigorous research and relentless investigation into popular poker apps like PPPOKER and XPoker led to a breakthrough\. We uncovered critical vulnerabilities, hidden pathways that were being exploited\. It was a revelation\.\n\n"
        "In November 2023, the *RevealApp* was born from this discovery\. Our mission? To level the playing field, to empower players like you with the ability to see what was once hidden – your opponents\' cards\.\n\n"
        "This isn\'t just a tool; it\'s a revolution in online poker\. Players worldwide are already gaining a strategic edge, transforming their gameplay and their winnings\. Now, it’s your turn to join them\.\n\n"
        "_Don\'t just play the game\. Change it\. Every moment without this insight is a missed opportunity to dominate\!_\n\n"
        "Intrigued?"
    )
    keyboard_config = [
        [{'text': "🚀 Be Part of This Revolution! Buy Now!", 'callback_data': 'how_to_buy_generic'}],
        [{'text': "✨ See All Advantages", 'callback_data': 'features_generic'}],
        [{'text': "🔙 Back to Previous Menu", 'callback_data': context.user_data.get('platform', 'start_over')}]
    ]
    reply_markup = build_keyboard(keyboard_config)
    await query.edit_message_text(text=story_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)

async def handle_testimonials(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    testimonials_text = (
        "🌟 *What Our Users Say About RevealApp* 🌟\n\n"
        "Don\'t just take our word for it\. Here\'s a glimpse of how RevealApp is changing the game for players around the globe:\n\n"
        "🗣️ _\'Since using the RevealApp, my win rate has skyrocketed\! I finally feel in control at the tables\. It paid for itself in the first week\!\'_ \- Alex R\., Professional Player\n\n"
        "🗣️ _\'I was skeptical at first, but RevealApp is the real deal\. Knowing my opponents\' cards is a game\-changer\. I\'m consistently cashing out big\.\'_ \- Maria S\., Poker Enthusiast\n\n"
        "🗣️ _\'This app is insane\! It\'s like having superpowers\. Easily the best investment I\'ve made for my poker game\. Highly recommended\!\'_ \- Chen L\., Online Grinder\n\n"
        "These are just a few voices from a growing community of winners\. Ready to write your own success story?"
    )
    keyboard_config = [
        [{'text': "🔥 I Want Results Like These! Buy Now!", 'callback_data': 'how_to_buy_generic'}],
        [{'text': "✨ See All Advantages", 'callback_data': 'features_generic'}],
        [{'text': "🔙 Back to Previous Menu", 'callback_data': context.user_data.get('platform', 'start_over')}]
    ]
    reply_markup = build_keyboard(keyboard_config)
    await query.edit_message_text(text=testimonials_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)

# --- Main Bot Logic ---
def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CallbackQueryHandler(start_command, pattern='^start_over$'))
    
    application.add_handler(CallbackQueryHandler(handle_platform_selection, pattern='^platform_(clubgg|xpoker|pppoker)$'))
    
    application.add_handler(CallbackQueryHandler(handle_how_to_buy, pattern='^how_to_buy_generic$'))
    application.add_handler(CallbackQueryHandler(handle_features, pattern='^features_generic$'))
    
    application.add_handler(CallbackQueryHandler(handle_faq, pattern='^faq$'))
    application.add_handler(CallbackQueryHandler(handle_contact_support, pattern='^contact_support$'))
    application.add_handler(CallbackQueryHandler(handle_story, pattern='^story$'))
    application.add_handler(CallbackQueryHandler(handle_testimonials, pattern='^testimonials$'))

    logger.info("Starting bot polling...")
    application.run_polling()

if __name__ == "__main__":
    main()

