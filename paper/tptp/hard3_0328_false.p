% hard3_0328  eq1=3069 eq2=153  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(f(f(f(X,Y),X),Y),Y) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(X,X),f(Y,X)) )).
