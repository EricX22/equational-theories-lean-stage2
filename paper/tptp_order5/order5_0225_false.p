% order5_0225  eq1=19539 eq2=58525  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(f(Y,Z),f(f(W,Z),f(U,U))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(f(X,Y),X) != f(Z,f(W,f(Y,X))) )).
