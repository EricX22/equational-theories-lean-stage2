% order5_0189  eq1=35409 eq2=16942  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(f(f(X,f(X,Y)),f(X,Y)),Y) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( X != f(Y,f(f(f(f(Z,W),U),Y),X)) )).
