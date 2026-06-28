% hard3_0234  eq1=2126 eq2=124  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(Y,Y),X),f(X,Z)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(Y,f(f(Y,X),X)) )).
