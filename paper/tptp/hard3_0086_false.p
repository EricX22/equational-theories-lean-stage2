% hard3_0086  eq1=646 eq2=4144  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(X,f(Y,f(f(Y,Z),Y))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,Y) != f(f(f(X,Z),Y),W) )).
