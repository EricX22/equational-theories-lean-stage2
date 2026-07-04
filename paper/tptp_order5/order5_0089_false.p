% order5_0089  eq1=45196 eq2=34797  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( f(X,X) = f(Y,f(f(f(Z,Y),W),U)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(f(Y,X),f(f(Z,X),Y)),W) )).
