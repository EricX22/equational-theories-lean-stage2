% hard3_0258  eq1=2451 eq2=2240  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(X,f(f(X,Y),Y)),Z) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(X,f(X,f(X,Y))),X) )).
