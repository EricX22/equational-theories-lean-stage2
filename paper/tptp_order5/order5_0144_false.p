% order5_0144  eq1=53021 eq2=59721  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,X) = f(f(f(f(Y,Y),X),X),Z) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( f(f(X,Y),Z) != f(Y,f(f(W,W),U)) )).
