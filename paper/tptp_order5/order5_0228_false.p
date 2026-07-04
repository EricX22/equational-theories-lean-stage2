% order5_0228  eq1=8810 eq2=61634  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(Z,f(f(f(Y,Y),Z),X))) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( f(f(X,Y),Z) != f(f(W,f(Z,U)),W) )).
