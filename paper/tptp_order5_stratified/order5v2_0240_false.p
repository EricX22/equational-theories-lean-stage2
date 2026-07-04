% order5v2_0240  eq1=40312 eq2=51353  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(f(Y,f(Z,X)),Y),W),W) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,X) != f(f(f(Y,Z),f(W,X)),X) )).
