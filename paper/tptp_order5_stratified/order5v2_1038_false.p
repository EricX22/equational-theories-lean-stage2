% order5v2_1038  eq1=19443 eq2=25841  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,Z),f(f(Z,W),f(Y,Y))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(X,f(f(Y,Y),X)),f(Z,W)) )).
