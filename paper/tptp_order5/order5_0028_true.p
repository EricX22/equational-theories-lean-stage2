% order5_0028  eq1=9073 eq2=42439  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,V,W,X,Y,Z] : ( X = f(Y,f(Z,f(f(f(W,U),V),X))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,X) = f(X,f(Y,f(f(Y,Z),Z))) )).
