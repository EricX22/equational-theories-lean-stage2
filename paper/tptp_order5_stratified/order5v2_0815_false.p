% order5v2_0815  eq1=12521 eq2=10574  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(Y,f(f(f(Z,W),Z),f(U,Z))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(Y,f(f(Z,Y),f(f(Z,X),Y))) )).
