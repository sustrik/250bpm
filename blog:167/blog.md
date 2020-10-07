# Simplest possible graph database

Each time one instantiates two structures in memory and connects them with a pointer, they have in fact created a simple graph database.

```go
type Person struct {
    Name     string
    Age      int
    Sex      string
    Father   *Person
    Mother   *Person
    Spouse   *Person
}

...

alice = &Person{Name: "Alice"}
bob = &Person{Name: "Bob", Mother: alice}
```

The users can't do any queries or any other fancy stuff but they can traverse the graph and inspect the fields in the structures.

```go
// Who is Bob's mother?
fmt.Println(bob.Mother.Name)
```

They can even save the database into a file using `json.Marshal` function from the `encoding/json` package and reload it at some later time. So far so good.

However, imagine that Carol and Dan are married:

```
carol = &Person{Name: "Carol"}
dan = &Person{Name: "Dan"}
carol.Spouse = dan
dan.Spouse = carol
```

This database can't be saved, because there's a loop in the graph. Marshalling algorithm would either enter an infinite loop or, possibly, realize that there is a loop and bail out.

Same problem occurs if one decides to add `Children` field to the structure so that it is possible to traverse the family tree in both directions.

In short, it would be nice to have a library, an equivalent of `encoding/json`, but one that is able to deal with the loops in the graph.

Obviously, it is not entirely trivial. First, the simple tree structure of JSON doesn't lend itself easily to representation of graphs. Second, there doesn't necessarily exist a single node from which every other node is reachable. The simple `json.Marshal(rootNode)` approach is not going to work.

Let's therefore add ability to store references in JSON like this:

```json
{
    "Person": {
        "CAROL": {
            "Name": "Carol",
            "Spouse": {"$ref": "Person:DAN"},
        },
        "DAN": {
            "Name": "Dan",
            "Spouse": {"$ref": "Person:CAROL"},
        }
    }
}
```

As for the problem with disconnected graphs, let's ask the user to create a "master" structure, i.e. a structure with pointers to all the nodes in the graph:

```go
type Master struct{
    Person []*Person
    Pet []*Pet
    // Add more node types here.
}
```

Once done the graph can be saved/loaded from JSON like this:

```go
var m1 Master
...
b, err := grison.Marshal(&m1)
...
var m2 Master
err = grison.Unmarshal(b, &m2)
```

Grison stands for "graph json" (but also happens to be a kind of [south-american wolverine](https://en.wikipedia.org/wiki/Galictis)) and the library can be found [here](https://github.com/sustrik/grison).

Interestingly, the JSON format with "typed" nodes allows for something that standard `encoding/json` can't do. It can unmarshal interfaces. The problem faced by `encoding/json` is that when it encounters an interface to unmarshal, it has no idea which concrete type to instantiate. The library just returns an error.

With grison format, however, the type is right there in the file (e.g. "Person"). And given that name "Person" is bound to type "Person" in the master structure, the library, when it encounters an interface pointer (marshaled as a grison reference) can easily infer the type of node to create.

**October 7th, 2020**

