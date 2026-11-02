from chatbot import SupportChatbot
from order_tool import OrderLookup
from stock_tool import StockLookup

def make_bot():
    """Build a fresh chatbot with its own tool for each test."""
    orders = {
        "A100": "shipped",
        "A101": "processing",
        "A102": "delivered"
    }
    stock = {
        "skirt": 10,
        "crop top": 5,
        "shorts": 0
    } 
    return SupportChatbot("Sunny", "Be friendly.", OrderLookup(orders), StockLookup(stock))

def test_tool_finds_known_status():
    tool = OrderLookup({"A100": "shipped"})
    assert tool.find_status("A100") == "shipped"

def test_tool_finds_unknown_status():
    tool = OrderLookup({"A100": "shipped"})
    assert tool.find_status("A123") is None

def test_respond_records_both_messages():
    bot = make_bot()
    bot.respond("Hello")
    assert len(bot.history) == 2
    assert bot.history[0]["role"] == "user"
    assert bot.history[1]["role"] == "assistant"

def test_order_question_uses_tool():
    bot = make_bot()
    assert bot.respond("What is the status of order A100?") == "Order A100 is shipped."

def test_order_question_without_id_prompts_for_id():
    bot = make_bot()
    assert "order ID" in bot.respond("What is the status of my order?")

def test_address_change_goes_to_human():
    bot = make_bot()
    assert "human" in bot.respond("I want to change the shipping address.")

def test_unknown_question_gets_safe_reply():
    bot = make_bot()
    assert "not sure" in bot.respond("What is the meaning of life?")

def test_two_chatbots_keep_separate_histories():
    first = make_bot()
    second = make_bot()
    first.respond("Hello")
    assert len(first.history) == 2
    assert len(second.history) == 0

#Exercise 2
def test_count_user_messages():
    bot = make_bot()
    bot.respond("hello")
    bot.respond("Where is order A100?")
    assert bot.count_user_messages() == 2

#Exercise 3
def test_stock_question_uses_the_stock_tool():
    bot = make_bot()
    assert "10" in bot.respond("Is the skirt in stock?")