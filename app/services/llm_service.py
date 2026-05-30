from google import genai
from google.genai import types


class LlmService:
    def __init__(self):
        self.client = genai.Client()

    def llm_response(self, query: str) -> str:
        prompt = """
 You are an expert interpreter. The attached transcript contains a possibly mix of English and another language or pure english. 

Please perform the following tasks:
1. Translate the entire text into uniform, professional English.
2. Provide a summary of the core takeaways.

### Mixed Transcript:
```text

"""
        prompt += query
        response = self.client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.5),
        )

        return response.text


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    obj = LlmService()
    print(
        obj.llm_response(
            query=""" The Steam Deck is arguably the best gaming handheld on the market. It has a great gaming experience, but its best part has always been its price point. This thing launched at $400, and the reason why Valve could price it so low is because they make mo

ney on every game that sold on the system. They have that like console, caliber, advantage. It was always cheap, but recently it got a hefty price bump. The one terabyte OLED model went up by 300 bucks from $649 to 949, and people were understandably 

upset. It's a 45% jump overnight, and it's not just Valve, it's Xbox pricing, PS5 pricing, RRG ally, even Nintendo who almost never raised their prices, jacked the price of the Switch 2 up by like 50 bucks before it even shipped. And in the computer s

pace, the cheaper entry level Mac Mini is gone, laptop prices are jacked up. It sucks, and the root of it is that memory and storage prices have skyrocketed, but I don't think most people realize how bad the memory saturation is. So 90% of the world's

 memory production is done by three companies. So Samsung and SK Heinix, those are both in South Korea, and then in the US, there's Micron. That's it. So three companies that make up 90% of the world's DRAM production. So there's various flavors of DR

AM and all of these companies make all the different flavors, but the big ones are DDR, so that's the kind of memory you'd see in desktops, then there's LPDDR, which is like low power DDR, and that's for like lower voltage, more energy efficient appli

cations, laptops and phones. And the third type is HBM. It stands for high bandwidth memory, and this stuff is the type of memory that you see in the Nvidia GPUs that run chat GPT. But the killer is that HBM modules require three times the factory cap

acity of DDR or LPDDR RAM. So in other words, for every gig of HBM that you produce, you could have produced three gigs of DDR or LPDDR. So regular RAM, like the stuff you'd see in the Steam Deck, a phone, a laptop, a desktop, that memory is essential

ly a flat chip. It comes from a big silicon wafer. It's one layer, and it's etched with billions of memory cells. They cut it up, they package it, and it gets used. And both DDR and LPDDR are done in the same way. But HBM is a different thing. It stil

l originates from a wafer, but HBM modules are built in a stack. They take eight, 12, sometimes 16 DRAM dies, and they stack them vertically, and then they drill thousands of channels straight through. And these channels allow the data to move up and 

down in parallel, which is why HBM memory is so high bandwidth. But this process of stacking is absolutely brutal on production rate, or like yields. Because when you stack dies, and even one of those layers has a defect, which is actually pretty comm

on, uh oh, too bad you got to dump the whole thing. And so yields on HBM modules are often low. Like 35 to 40% of HBM output is burnt. It uses a lot of factory capacity. And because it's so wickedly expensive and time consuming and it's difficult to m

ake, companies charge a lot of money for it. And the profit margins on HBM is way higher than DDR or LPDDR. And so a lot of factories have shifted their production to HBM. And as a result, for regular memory, since there's less of it being made and th

ere's still strong demand, the price of it goes up and up and up until you have a nearly $1,000 steam deck, which is seemingly crazy. But it's not like Valve being greedy here. The price of the memory and the storage inside this device are probably tr

iple of what they want it to be. So this is how they're reacting to it. Now, if there was one company, or one group of companies to point the finger at, it would be the memory manufacturers, right? They're the ones that decides to reallocate their pro

duction to HBM. They're the ones that are setting the price of a regular DDR and LPDDR. And if they wanted to, they're the ones that could theoretically switch back to making this kind of memory and just have normal pricing. But the memory industry is

 like a graveyard. In the 90s, there were so many DRAM makers, but today, there are three big ones left. The rest of them either got bought out or they died for making the same mistake of making too much memory. Because when you make too much, demand 

goes down, price goes down, and the industry just collapses. So for the guys that remain, SK Hinex, Samsung, Micron, they know that the number one rule that you never break is never make enough memory. Always make sure that demand is unmet so the pric

es can spike and keep you in business. Because the alternative is to make enough memory and then it's over. The party is over. So when AI showed up and was like, hey, we can offer you guys the fattest profits you've ever seen if you make HBM. So they 

all transitioned. They've all switched over to, because that's just the nature of the business. Now, we've seen expensive RAM for a couple of years now. A very expensive gaming handheld, I think is the least of our problems. I think it gets way worse.

 Let me show you some numbers. So SK Hinex is fully booked for the RAM production for the rest of the year, mostly to NVIDIA. Also, OpenAI has this massive data center project called Stargate, and that thing is projected to require 900,000 wafers per 

month of DRAM. Like that is 40% of the global production of these wafers being sent to one project. And that's just for OpenAI, the guys that handle chat GBT. All the other AI providers and all the other hyperscalers like Microsoft, MATA, like everybo

dy wants this RAM. So I think we're gonna have supply issues for years. Now, the first reaction I'd have is like, if this is the case, why don't they just make more production facilities, right? Well, like I described before, most memory companies do 

not want to over invest and get burned, because these things are expensive. These facilities are like 15, 20 billion to make. It's like crazy, but they have started it, but keep in mind, these facilities take like four or five years to come up to oper

ation. And even when they're running, the first couple years have terrible yields. So this thing, like this issue is so, it goes so deep and for so long. Now, one thing we're already starting to see is this trend of lowered specs. So we're starting to

 see entry-level Windows laptops being reverted back to eight gigs of RAM and reduced storage just to keep the prices tolerable. But eight gigs of RAM in a Windows laptop in 2026 is just not good. And keep in mind that a lot of modern laptops have RAM

 that soldered on. You can't ever upgrade it. It's baked on, so you're stuck with the life of that product. With eight gigs of RAM on a Windows laptop that you bought in 2026. That's just the worst. It's so bad. And if we're seeing the same kind of st

uff in the phone market, we're seeing new devices, at least they're rumored to have less RAM than the previous generation. And this is for entry-level stuff and like mid to your stuff, high-end stuff is like we're likely going to see elevated pricing.

 Now, the second thing that's coming from this is that the used market is just getting decimated. Like when new stuff goes up in price, usually the used market follows and it just bumps up. But this is seeing such escalated pricing that people are hol

ding on to their devices for longer because they don't want to upgrade. And so there's less devices even entering the used market. And the price of that stuff is just way higher than it used to be. And it's really painful to see. And the third thing t

hat I think is really important, but almost difficult to talk about is just, okay, when the new price is revealed and it's super expensive, usually people complain about it, pretty aggressively upfront. But then after a while, it kind of like people g

et complacent and then that super expensive new price becomes just the normal price. The best example that I can think of is like the 20 series gaming laptops. When those first came out, I made so many videos being like, this is crazy pricing. These 2

0 series gaming laptops, let's say like a 2070 or 2080, those things are like 50% more than the 10 series stuff for like 15% better. Sometimes like 10% better. And I was like, super expensive, don't buy the stuff is not worth it. People in the beginni

ng agreed, they're like, yeah, it's super expensive. But then enough people bought it and then they became the normal price. People are like, yeah, this is just the way it is. And so when that happens, like this is a gaming handheld that jumped up by 

40%, 45% in price. And I just checked before I started shooting this video. These things are sold out. This thing, like people complain, they're like, oh my god, this is crazy. How is it? How is it $300 more than it was yesterday? And then today it's 

sold out. What is it? It just, this is just the way it is. And when more and more people buy these things and just accept that price and it's not valid, right? It's the markets of the world that are influencing this. But it becomes the norm. And it ne

ver comes back down. Look at desktop GPUs. When the 5091s came out with its $2,000 MSRP, people were outraged at the price. They were like, this is crazy. And then people got used to it, people bought it. And now you can't even keep a 5090 on the shel

f. It pops up, it gets sold immediately because at this point, a $2,000 5090s arguably a good price. And here's the thing. I made this video because when I saw the price of the steam that go up, I had this like sick, almost visceral reaction to it. Be

cause I thought if there was one product that would be able to withstand the whole RAM and storage price bump, it would be this thing. Because Valve has their steam store, they can subsidize the cost of this with steam sale or game sales. And even Val

ve got hit. I'm like, holy. So this is just like a brain dump. I hope you guys enjoyed this video. I hope you learned something from it. But this is just my kind of immediate reaction to this whole steam deck going up in price.

summarise this """
        )
    )
