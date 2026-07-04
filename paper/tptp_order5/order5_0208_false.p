% order5_0208  eq1=31134 eq2=26330  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(X,f(f(Y,Z),f(X,X))),W) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(Y,f(f(Z,Y),X)),f(Y,Y)) )).
