% order5_0074  eq1=34214 eq2=37681  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(f(f(Y,Z),f(X,f(W,U))),Z) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(f(Y,f(Z,f(X,Y))),W),W) )).
