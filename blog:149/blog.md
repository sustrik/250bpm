# Programmatic Code Generation: Composability

After working some more with [Tiles](https://github.com/sustrik/tiles), my mini-library for programmatic code generation, I've realized it has a feature that I haven't knowingly baked in, but which makes it a really good tool for the job. Namely, the code you write is composable.

Here's what I mean: If you want to generate a C function that prints out names of countries' capitals then you can generate the code that does the actual printing first:

    data = {
        "Afghanistan": "Kabul",
        "Brazil": "Brasilia",
        "Canada": "Ottawa",
    }
    
    body = t/''
    for country, capital in data.items():
        body |= t/"""
                  printf("@{capital} is the capital of @{country}");
                  """

Once done, you cen generate the scaffolding:

    program = t/"""
        #include <stdio.h>
    
        int main(void) {
            @{body}
            return 0;
        }
        """

The example, of course, shows just two levels of nesting. In practice, however, you'd have many levels of nesting.

But whatever the nesting level, you, as a programmer, can focus on a single task at a time. First, you think about how to print the capitals. Then you think about the scaffolding. There's no overlap.

Compare that to your typical templating solution:

    template = Template("""
        #include <stdio.h>
    
        int main(void) {
            {% for country, capital in data.items() %}
            printf("{{ capital }} is the capital of {{ country }}");
            {% endfor %}
            return 0;
        }
        """)
    template.render(data=data)

Note how you start with writing scaffolding (include, main) then you switch to the business logic (printf), then you get back to scaffolding (return).

The example is trivial and as such, the both solutions are kind of comparable.

However, imagine there are five levels of nesting.

The code written using Tiles would, logically, look like this:

    level1
    level2
    level3
    level4
    level5

The code written using one the classic templating tools, on the other hand, would look like this:

    level1
      level2
        level3
          level4
            level5
          level4
        level3
      level2
    level1

**March 2nd, 2019**