% hard3_0214  eq1=2042 eq2=2692  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(X,X),Y),f(X,Z)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(f(X,Y),f(Z,W)),Y) )).
