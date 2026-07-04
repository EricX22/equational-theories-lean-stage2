% order5_0029  eq1=42619 eq2=603  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( f(X,Y) = f(X,f(X,f(f(Y,X),X))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(Y,f(Z,f(W,f(W,X)))) )).
