% order5_0214  eq1=14566 eq2=48267  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(f(f(X,X),f(Z,X)),Y)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(f(Z,f(Y,Y)),f(X,X)) )).
