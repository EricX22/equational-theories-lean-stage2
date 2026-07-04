% order5v2_0368  eq1=30017 eq2=6908  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(f(Y,f(Z,f(W,f(Y,X)))),U) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(Y,f(Y,f(f(Z,Y),f(W,Z)))) )).
