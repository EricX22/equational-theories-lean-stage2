% hard3_0279  eq1=2668 eq2=3530  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(X,Y),f(X,Z)),W) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(X,f(f(Z,X),Z)) )).
