#

||
|---|
|![Banner](/assets/banner-sprint4-desafio.png)|
||

## SEÇÕES

## (ALGUNS) PRINCÍPIOS DE ARQUITETURA DE MICROSSERVIÇOS

Immutability
Cockcroft says the principle of immutability is used at Netflix to assert that autoscaled groups of service instances are stateless and identical, which enables Netflix’s system to “scale horizontally.” The Chaos Monkey, a member of the Simian
Army, removes instances regularly to enforce the immutable stateless service
principle. Another related technique is the use of “Red/Black pushes”. Although
each released component is immutable, a new version of the service is introduced
alongside the old version, on new instances, then traffic is redirected from old to
new. After waiting to be sure all is well, the old instances are terminated. (NADAREISHVILI et al, 2016, p. 45)

The container is instantiated from its image,
and then the contents of the container should not change. Any executables or depen‐
dencies that the application code needs should be included in that image. We dis‐
cussed this earlier through the lens of vulnerability detection: you can’t scan for
vulnerabilities in code that isn’t included in the image, so you should make sure that
everything you want to scan is included. (RICE, 2020, p. 155)


Build afresh
The second part of McIlroy’s first principle (“build afresh”) is also important. Part
of the Unix philosophy is to create a collection of powerful tools that are predict‐
able and consistent over a long period of time. It is worth considering this as an
additional principle when implementing microservices. It may be better to build
a new microservice component rather than attempt to take an existing compo‐
nent already in production and change it to do additional work. This also maps to
Netflix’s immutability principle. (NADAREISHVILI et al, 2016, p. 47)

- Não hesite em descartar

Don’t hesitate to throw it away
This is a difficult one for some developers. Being willing to throw something
away can be hard when you’ve spent a great deal of time and effort building a
component. However, when you adopt the “try early” principle, throwing away
the early attempts is easier.
It is also important to consider this “throw it away” principle for components that
have been running in production for a long time. Over time, components that
did an important job may no longer be needed. You may have applied the “build
afresh” principle and replaced this component with one that does the job better. It
may be the case that the “one thing” that component does is simply no longer
needed. The important thing is to be willing to throw away a component when it
no longer serves its intended purpose. (NADAREISHVILI et al, 2016, p. 48)

### BOAS PRÁTICAS DE CONTEINERIZAÇÃO

Run One Application per Container
Always run a single application within a container. Containers were
designed to run a single application, with the container having the same life
cycle as the application running in the container. Running multiple
applications within the same container makes it difficult to manage, and you
might end up with a container in which one of the processes has crashed or
is unresponsive. (JAUSOVEC, SCHOLLp. 249)
