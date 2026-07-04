% order5v2_0505  eq1=18348 eq2=23019  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(f(Y,Y),f(Z,f(f(W,W),U))) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( X != f(f(Y,f(Z,W)),f(f(Y,U),Z)) )).
