% order5_0030  eq1=39421 eq2=10749  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(f(Y,Z),f(X,Y)),X),Y) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( X != f(Y,f(f(Z,W),f(f(Z,X),U))) )).
