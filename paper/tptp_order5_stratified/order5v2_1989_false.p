% order5v2_1989  eq1=22850 eq2=29656  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(f(Y,f(Z,Y)),f(f(Y,W),U)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(Y,f(Y,f(Y,f(Y,Y)))),Y) )).
