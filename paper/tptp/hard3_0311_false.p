% hard3_0311  eq1=2892 eq2=4119  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(X,f(Y,Z)),Z),Z) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(f(f(X,X),X),Z) )).
