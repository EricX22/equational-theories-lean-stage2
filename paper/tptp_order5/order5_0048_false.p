% order5_0048  eq1=31481 eq2=59851  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(f(Y,Z),f(Z,W))),Z) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( f(f(X,Y),Z) != f(W,f(f(Y,U),X)) )).
