% hard3_0188  eq1=1679 eq2=3334  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(X,Y),f(f(Z,W),W)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(X,f(Z,f(Z,Y))) )).
