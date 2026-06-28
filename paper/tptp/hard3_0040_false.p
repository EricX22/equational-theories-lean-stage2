% hard3_0040  eq1=215 eq2=3050  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(X,f(Y,Z)),Y) )).
fof(neg, negated_conjecture, ? [X] : ( X != f(f(f(f(X,X),X),X),X) )).
