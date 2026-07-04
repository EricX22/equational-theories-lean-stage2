% order5v2_0557  eq1=23928 eq2=57599  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(Y,Z),W),f(W,f(X,Z))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,f(Y,X)) != f(f(f(Z,X),Y),W) )).
