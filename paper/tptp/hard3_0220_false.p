% hard3_0220  eq1=2069 eq2=1635  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(X,Y),Y),f(Z,W)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(X,X),f(f(Y,X),Y)) )).
