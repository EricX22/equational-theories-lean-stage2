% order5v2_1484  eq1=6392 eq2=26409  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(Z,f(W,f(f(W,Y),Y)))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(Y,f(f(Z,Z),X)),f(Y,W)) )).
