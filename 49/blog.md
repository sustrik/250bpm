# Reusability Trap



Truly reusable components are clearly separated from the code that uses them. That makes it easy to use the component in a different project. It also makes it easy to rip the component out and replace it by a different one.

Non-reusable components cannot be used in different projects. At the same time, they tend to be hairy and almost impossible to rip out of their native project. They are interconnected with the rest of the codebase in subtle ways. Replacing them can break the functionality in unexpected manners and even if it does not you can never be sure that there's no hidden problem waiting for the most inconvenient time to strike you.

In a long-lived project, components are being replaced. Nice reusable components are easy to replace and so they are. Ugly non-reusable components are pain to replace and each replacement means both a considerable risk and considerable cost. Thus, more often then not, they are not replaced. As the years go by, reusable components pass away and only the hairy ones remain. In the end the project turns into a monolithic cluster of ugly components melted one into another.

This mechanism seems to account for most of the complexity in legacy codebases.

Let's call it Sustrik's law:

**"Well-designed components are easy to replace. Eventually, they will be replaced by ones that are not so easy to replace."**

The law seems almost impossible to beat. Are there any policies users can adopt to avoid the trap? Is there anything developers of nice components can do to avoid being replaced? I would love to hear any suggestions.

**Martin Sústrik, June 2nd, 2015**