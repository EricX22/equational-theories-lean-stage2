% order5_0239  eq1=8169 eq2=20392  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(Y,f(Z,f(f(W,f(U,X)),W))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(Y,Z),f(f(W,f(Z,X)),X)) )).
