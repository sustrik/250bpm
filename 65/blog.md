# Ecology of Software Quality



I've read a nice article about [economics of software correctness](http://www.drmaciver.com/2015/10/the-economics-of-software-correctness/) a recently.

It was a nice reminder that we are often forgetting about economics when dealing with the minutiae of our industry.

However, let me try to paint a bit broader picture, dealing not only with software correctness but software quality in general.

It's no secret that basically all the code we have is a mess. And that's putting it bluntly. Lot of people would choose more expressive language to describe the status quo.

So what's the reason for that?

As the article linked above argues, there's a cost to finding and fixing a bug and that cost is often prohibitive. And why is it so expensive? Because the code quality is poor. Code we deal with is a patchwork of buggy technologies hastily assembled together using duct tape. So, one would argue, improving the overall quality of code would lead to more maintainable systems and drive the cost of bug fixing down to sustainable levels.

And here's where it gets interesting.

Imagine you are an IT manager and you have a limited budget for doing engineering work. How would you spend it?

On one hand, you can invest in code quality. You ask the engineers to do code clean-ups, refactoring and so on. What you get is more maintainable codebase, which means you can fire, say, 20% of the department. Great! You have just reduced the cost by 20%.

On the other hand, you can ask them to implement a new feature. The code quality would stay poor but the new feature will attract more users. Great! You have just increased the userbase and thus the revenue by 20%.

What you'll really do depends on the ratio of these two numbers. In reality, they won't be equal and they won't be 20% either.

And when you look at the software landscape today, the number of users scales exponentially with respect to number of developers. We are in a phase of explosive growth. If you try to save costs, you can fire a half of IT department, but it's peanuts compared to what you can possibly get when focusing on delivering features: You can grow the revenue by whole orders of magnitude.

In the end, there's little question about what to invest in.

The above is bad news for software quality, but turning a blind eye on the problem won't solve it. This way we can at least speak about it and reason about it.

For example: Do we have good models for what's happening? Well, yes. It turns out that ecology have studied this kind of dynamics for decades.

To draw a parallel to software development, there are opportunistic species that take advantage of new niches (say a new clearing in the forest) and try to fill it as fast as possible, even at the cost of being fragile and prone to physical damage, diseases and so on. If the niche is stable, the opportunistic species are overtaken by so called climax species which invest heavily in "quality". They may not grow so fast, but they are going to survive next storm or next extra-chilly winter.

In central Europe you can compare Tree of Heaven (Ailanthus Altissima) which is an invasive tree species growing up at astounding speed to common oak (Quercus Robur) which dominates old forests. The difference in "quality" is quite large. While the wood of Ailanthus breaks easily, sawing through an oak plank is requires a non-trivial amount of physical strength. Unsurprisingly Ailanthus' lifespan is approximately 60-80 years while oak can survive for 500 or even 800 years.

So, can we expect the software niches to be filled eventually and opportunistic software to give way to quality climax software?

I don't see it happening any time soon. There's still too much empty space to fill. It's still Wild West and unlimited horizons down here.

However, we shouldn't get desperate. Software isn't going to grow on forever. Consider steam engines. At their heyday one would say there was no end to their expansion. Yet, today, steam engines are a pretty small and stable niche seeing little growth. When we'll eventually get there, we'll finally have time to write some beautiful, well-designed and bug-less code.

**October 14th, 2015**