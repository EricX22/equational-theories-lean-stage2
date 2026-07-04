% order5v2_1468  eq1=7657 eq2=4976  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(X,f(f(Z,f(W,X)),W))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(Y,f(X,f(Z,f(X,f(Y,X))))) )).
