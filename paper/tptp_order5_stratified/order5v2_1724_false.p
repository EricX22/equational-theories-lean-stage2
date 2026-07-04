% order5v2_1724  eq1=35093 eq2=23461  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(f(f(Y,Z),f(f(X,W),U)),U) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( X != f(f(f(Y,X),Z),f(W,f(U,Y))) )).
