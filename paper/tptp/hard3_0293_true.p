% hard3_0293  eq1=2787 eq2=466  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(Y,Z),f(Y,X)),X) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(Y,f(X,f(X,f(Y,X)))) )).
