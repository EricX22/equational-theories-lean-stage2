% order5v2_0568  eq1=18423 eq2=18426  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,Z),f(X,f(f(W,W),Z))) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( X != f(f(Y,Z),f(X,f(f(W,U),X))) )).
