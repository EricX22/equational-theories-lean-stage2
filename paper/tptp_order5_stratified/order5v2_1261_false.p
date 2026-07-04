% order5v2_1261  eq1=29252 eq2=32923  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(f(X,f(X,f(X,f(X,X)))),Y) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(X,f(f(f(Y,Z),Z),Y)),X) )).
