% order5_0159  eq1=37841 eq2=19562  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(Y,f(Z,f(Z,Z))),Y),X) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( X != f(f(Y,Z),f(f(W,W),f(U,Y))) )).
