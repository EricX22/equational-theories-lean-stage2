% order5_0096  eq1=2252 eq2=56793  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(X,f(X,f(Y,Z))),W) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,f(Y,Y)) != f(f(X,f(X,X)),Y) )).
