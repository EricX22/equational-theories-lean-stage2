% order5v2_0515  eq1=21866 eq2=53697  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(Z,X)),f(X,f(X,W))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,Y) != f(f(f(f(Z,W),Y),Y),X) )).
